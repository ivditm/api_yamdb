# Generated by Django 3.2 on 2023-03-23 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20230323_0932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ['pub_date'], 'verbose_name': 'комментарий', 'verbose_name_plural': 'коментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'ordering': ['pub_date'], 'verbose_name': 'отзыв', 'verbose_name_plural': 'отзывы'},
        ),
    ]
