# Generated by Django 4.2.1 on 2023-05-25 14:45

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bbsh_api", "0009_remove_basket_name_remove_basket_size_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basket",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="history",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="orderlist",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
