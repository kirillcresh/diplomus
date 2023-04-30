from django.db import models
from django.contrib.auth.models import User
from datetime import *


class News(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='Автор публикации')
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name='Заголовок')
    news = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(default=datetime.now)
    picture = models.ImageField(upload_to='images/')

    def get_absolute_url(self):
        return f'/news/{self.id}/'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

