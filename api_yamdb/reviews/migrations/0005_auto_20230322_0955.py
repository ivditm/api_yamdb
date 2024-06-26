# Generated by Django 3.2 on 2023-03-22 06:55

import django.core.validators
from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'ordering': ['pub_date']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'ordering': ['name'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления отзыва'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(db_index=True, help_text='введите название, произведения', max_length=256, verbose_name='наименование произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='введите год выпуска', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2023)], verbose_name='год выпуска'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите имя пользователя', max_length=150, unique=True, validators=[reviews.models.validate_username]),
        ),
    ]
