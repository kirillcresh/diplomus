# Generated by Django 4.1.4 on 2022-12-26 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_comment_game'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
