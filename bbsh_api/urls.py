from django.urls import path

from bbsh_api import views

urlpatterns = [
    path("livez/", views.server_is_healthy),
    path("login/", views.user_login),
    path("logout/", views.user_logout),
    path("registration/", views.user_registration),
    path("menu/", views.show_menu),
    path("<uuid:user_id>/basket/", views.user_basket),
    path("<uuid:user_id>/basket/add/", views.user_basket_add),
    path("<uuid:user_id>/basket/delete/", views.user_basket_delete),
    path("<uuid:user_id>/make_order/", views.user_make_order),
    path("<uuid:user_id>/order_info/", views.get_order_info),
    path("<uuid:user_id>/history/", views.user_history),
    path("<uuid:user_id>/profile/", views.user_profile),
    path("<uuid:user_id>/profile/delete/", views.user_profile_delete),
    path("<uuid:staff_id>/menu/add_new/", views.menu_add),
    path("<uuid:staff_id>/menu/delete/", views.menu_delete),
    path("<uuid:staff_id>/order_list/show_all/", views.show_all_orders),
    path("<uuid:staff_id>/order_list/accept_order/", views.accept_order),
    path(
        "<uuid:staff_id>/order_list/dismiss_order/",
        views.dismiss_order,
    ),
    path(
        "<uuid:staff_id>/order_list/order_is_ready/",
        views.ready_order,
    ),
    path("<uuid:staff_id>/history_all/", views.show_all_history),
    path("<uuid:staff_id>/users/get_user_info/", views.get_user_info),
]
