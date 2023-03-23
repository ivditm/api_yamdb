from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

import re
import datetime

PATTERN_USER = r'^[\w.@+-]+\Z'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
FIRST_NAME_MAX_LENGTH = 150
LAST_NAME_MAX_LENGTH = 150
ROLE_CHOICE_MAX_LENGTH = 9
NAME_MAX_LENGHT = 256
SLUG_MAX_LENGHT = 50
ROLE_CHOICES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]
YEAR_VALIDATION_ERROR_MESSAGE = ('Книга не может быть из будущего или '
                                 'выпущена динозаврами')


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" для имени пользователя'
        )
    elif not re.match(PATTERN_USER, value):
        raise ValidationError(
            'Имя пользователя не соответствует паттерну'
        )
    return value


def validate_year(value):
    if 0 < value <= datetime.datetime.now().year:
        return value
    else:
        raise ValidationError(YEAR_VALIDATION_ERROR_MESSAGE)


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Введите имя пользователя',
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        help_text='Введите email'
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        help_text='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        help_text='Фамилия',
        blank=True
    )
    bio = models.TextField(
        help_text='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=ROLE_CHOICE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER
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
        ordering = ('username',)
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
    name = models.CharField(max_length=NAME_MAX_LENGHT,
                            verbose_name='категория',
                            help_text='введите категорию')
    slug = models.SlugField(unique=True,
                            max_length=SLUG_MAX_LENGHT,
                            verbose_name='уникальный слаг',
                            help_text='придумайте слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGHT,
                            verbose_name='жанр',
                            help_text='введите жанр')
    slug = models.SlugField(unique=True,
                            max_length=SLUG_MAX_LENGHT,
                            verbose_name='уникальный слаг',
                            help_text='придумайте слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGHT,
                            db_index=True,
                            verbose_name='наименование произведения',
                            help_text='введите название, произведения')
    year = models.PositiveSmallIntegerField(verbose_name='год выпуска',
                                            validators=(validate_year,),
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
        ordering = ['name']
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


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name='жанр')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='произведение')

    class Meta:
        verbose_name = 'связь жанра и произведения'
        verbose_name_plural = 'соответствие жанров и произведений'

    def __str__(self) -> str:
        return f'{self.title} является {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    text = models.TextField("Текст", help_text="Отзыв")
    pub_date = models.DateTimeField(
        'Дата добавления отзыва',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta:
        ordering = ['pub_date']
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['pub_date']
        default_related_name = 'comments'
