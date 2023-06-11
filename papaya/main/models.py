from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    tickets = models.IntegerField(default=0, verbose_name="Количество лотерейных билетов")
    client_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.client_id)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
