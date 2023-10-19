import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import *


class Category(models.Model):
    category = models.CharField(max_length=60)
    description = models.TextField(default='Эта категория вам понравится', verbose_name='Описание категории')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Games(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name='Название игры')
    games = models.TextField(verbose_name='Описание игры')
    picture = models.ImageField(upload_to='images/')
    category_class = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name='Категория товара')
    price = models.FloatField(default=1000, verbose_name='Цена')
    components = models.TextField(default='Отсутствуют', verbose_name='Компоненты')
    min_players = models.IntegerField(default=1, verbose_name='Минимальное количество игроков')
    max_players = models.IntegerField(default=2, verbose_name='Максимальное количество игроков')
    recommend_age = models.IntegerField(default=4, verbose_name='Рекомендуемый возраст')
    game_time = models.IntegerField(default=40, verbose_name='Среднее время игры')
    vendor = models.TextField(default='PapayaGames', verbose_name='Производитель')
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    is_active = models.BooleanField(default=True, verbose_name='Существует')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        db_table = "games"

    def get_absolute_url(self):
        return f'/shop/{self.id}/'

    def get_discount_price(self):
        discount_price = int(self.price * (100 - self.discount) / 100)
        return discount_price

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='Автор комментария')
    game = models.ForeignKey(Games, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.CharField(null=False, blank=False, max_length=500, verbose_name='Комментарий')
    pub_date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=5, null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
