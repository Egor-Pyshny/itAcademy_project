# Generated by Django 4.2.1 on 2023-05-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bbsh_api", "0003_menu"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="points",
            field=models.IntegerField(default=0),
        ),
    ]
