from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    year = models.IntegerField(validators=(MinValueValidator(0),
                                           MaxValueValidator(3000)),
                               verbose_name='год выпуска',
                               help_text='введите год выпуска')
    description = models.TextField('описание произведения',
                                   help_text='добавьте описание')
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
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

    def __str__(self) -> str:
        return self.name
