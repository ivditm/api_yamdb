# Generated by Django 3.2 on 2023-03-15 17:07

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='введите категорию', max_length=256, verbose_name='категория')),
                ('slug', models.SlugField(help_text='придумайте слаг', unique=True, verbose_name='уникальный слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='введите жанр', max_length=256, verbose_name='жанр')),
                ('slug', models.SlugField(help_text='придумайте слаг', unique=True, verbose_name='уникальный слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='введите название, произведения', max_length=100, verbose_name='наименование произведения')),
                ('year', models.PositiveSmallIntegerField(help_text='введите год выпуска', verbose_name='год выпуска')),
                ('description', models.TextField(help_text='добавьте описание', verbose_name='описание произведения')),
                ('category', models.ForeignKey(blank=True, help_text='категория,к которой будет относиться произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='категория')),
                ('genre', models.ManyToManyField(blank=True, db_index=True, help_text='добавьте жанр', related_name='titles', to='reviews.Genre', verbose_name='жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ['year'],
                'default_related_name': 'titles',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='Введите имя пользователя', max_length=150, unique=True)),
                ('email', models.EmailField(help_text='Введите email', max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, help_text='Имя', max_length=150)),
                ('last_name', models.CharField(blank=True, help_text='Фамилия', max_length=150)),
                ('bio', models.TextField(blank=True, help_text='Биография')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=20)),
                ('confirmation_code', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.CheckConstraint(check=models.Q(year__lte=2023), name='проверка на год выпуска'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_fields'),
        ),
    ]
