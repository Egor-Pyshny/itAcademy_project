import sqlite3
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
from django.core.mail import send_mail

from bbsh_api.models import History, MyUser, OrderList

app = Celery(
    "periodic.m63",
    broker="redis://broker:6379/",
)
app.set_default()


@app.task
def send_day_statistics():
    admin_mail = MyUser.objects.filter(user="admin").email
    today = str(datetime.now().date()) + " 00:00:00"
    res = History.objects.filter(date_time=f"{today}")
    stat = ""
    for order in res:
        stat = str(order) + "\r\n"
    send_mail(
        "Statistics for "
        + str(datetime.now().year)
        + "."
        + str(datetime.now().month)
        + "."
        + str(datetime.now().day),
        stat,
        "autosend@mail.ru",
        [admin_mail],
        fail_silently=False,
    )


@app.task
def clear_order_list():
    OrderList.objects.delete()
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    sql = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'bbsh_api_orderlist';"
    cursor.execute(sql)


@app.task
def clear_history_list():
    # one_year_ago = timezone.now() - timezone.timedelta(days=365)
    # one_year_ago = one_year_ago.date()
    History.objects.delete()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **_kwargs: dict):
    sender.add_periodic_task(
        crontab(minute="55", hour="23"),
        send_day_statistics,
    )
    sender.add_periodic_task(
        crontab(minute="55", hour="23"),
        clear_order_list,
    )
    sender.add_periodic_task(
        crontab(minute="55", hour="23"),
        clear_history_list,
    )
