from django.db import models
from django.contrib.auth.models import User
from datetime import *


class Category(models.Model):
    category = models.CharField(max_length=60)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Games(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name='Заголовок')
    games = models.TextField(verbose_name='Текст')
    picture = models.ImageField(upload_to='images/')
    category_class = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=1000, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Существует')


    def get_absolute_url(self):
        return f'/shop/{self.id}/'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Comment(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='Автор комментария')
    game = models.ForeignKey(Games, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.CharField(null=False, blank=False, max_length=500, verbose_name='Комментарий')
    pub_date = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'