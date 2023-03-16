from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text='Введите email'
    )
    first_name = models.CharField(
        max_length=150,
        help_text='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        help_text='Фамилия',
        blank=True
    )
    bio = models.TextField(
        help_text='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    password = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_fields'
            )
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='категория',
                            help_text='введите категорию')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='уникальный слаг',
                            help_text='придумайте слаг')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='жанр',
                            help_text='введите жанр')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='уникальный слаг',
                            help_text='придумайте слаг')

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='наименование произведения',
                            help_text='введите название, произведения')
    year = models.PositiveSmallIntegerField(verbose_name='год выпуска',
                                            help_text='введите год выпуска')
    description = models.TextField('описание произведения',
                                   help_text='добавьте описание')
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   db_index=True,
                                   verbose_name='жанр',
                                   help_text='добавьте жанр')
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 db_index=True,
                                 verbose_name='категория',
                                 help_text=('категория,'
                                            'к которой будет '
                                            'относиться произведение'))

    class Meta:
        ordering = ['year']
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=datetime.datetime.now().year),
                name='проверка на год выпуска'
            )
        ]

    def __str__(self) -> str:
        return self.name
