from django.db import models
from django.contrib.auth.models import User
from datetime import *
from shop.models import Games


class DeliveryPoint(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    work_hours = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'delivery_point'
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'


class Orders(models.Model):
    is_cart = models.BooleanField(default=True)
    total = models.IntegerField(null=True, default=0)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=50, default='88002200220')
    delivery_address = models.ForeignKey(DeliveryPoint, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return f'/orders/{self.id}/'

    def __str__(self):
        return str('Заказ № ' + str(self.id))

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProducts(models.Model):
    games_id = models.ForeignKey(Games, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(str(self.order_id) + ', Игра: ' + str(self.games_id))

    class Meta:
        db_table = 'order_products'
        verbose_name = 'Игра в заказе'
        verbose_name_plural = 'Игры в заказе'
