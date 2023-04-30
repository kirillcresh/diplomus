from django.db import models
from django.contrib.auth.models import User
from datetime import *
from shop.models import Games


class Orders(models.Model):
    is_cart = models.BooleanField(default=True)
    total = models.IntegerField(null=True, default=0)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return f'/orders/{self.id}/'

    def __str__(self):
        return str('Заказ № ' + str(self.id))

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProducts(models.Model):
    games_id = models.ForeignKey(Games, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(str(self.order_id) + ', Игра: ' + str(self.games_id))

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'