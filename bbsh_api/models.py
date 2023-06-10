from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    phone = models.CharField(blank=False, max_length=13)
    id = models.UUIDField(primary_key=True, default=uuid4)

    def to_dict(self):
        return {
            "username": self.get_username(),
            "phone": self.phone,
            "id": self.id,
        }


class Menu(models.Model):
    name = models.TextField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    size = models.TextField(blank=False, null=False)
    ingredients = models.TextField(blank=False, null=False)

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "cost": self.cost,
            "ingridients": self.ingredients,
        }


class Basket(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    dish = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    dop_ingredients = models.TextField(blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "name": self.dish.name,
            "cost": self.dish.cost,
            "size": self.dish.size,
            "dop_ingredients": self.dop_ingredients,
            "id": str(self.id),
            "user_id": str(self.user.id),
        }


class History(models.Model):
    name = models.TextField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    size = models.TextField(blank=False, null=False)
    dop_ingredients = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=False, null=False)
    user = models.UUIDField()
    id = models.UUIDField(default=uuid4, primary_key=True)
    comments = models.TextField(default="")

    def to_dict(self):
        return {
            "name": self.name,
            "cost": self.cost,
            "size": self.size,
            "dop_ingredients": self.dop_ingredients,
            "date_time": self.date_time,
            "user_id": self.user,
        }

    def __str__(self):
        return (
            f"Название: {self.name}, "
            f"размер: {self.size}, "
            f"цена: {self.cost}, "
            f"дополнительные ингридиенты: {self.dop_ingredients}"
        )


class OrderList(models.Model):
    dish = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    dop_ingredients = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=False, null=False)
    accepted = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    order_id = models.IntegerField(blank=False, null=False)
    comments = models.TextField(default="")

    def to_dict(self):
        return {
            "dish": self.dish.name,
            "dop_ingredients": self.dop_ingredients,
            "date_time": self.date_time,
            "accepted": self.accepted,
            "ready": self.ready,
            "user_id": self.user.id,
            "order_id": self.order_id,
        }
