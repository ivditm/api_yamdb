import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

import datetime


from reviews.models import User, Genre, Category, Title

PATTERN_USERS = re.compile(r'[\\w.@+-]+\\z')
ERROR_MESSAGE_TITLE = 'год выпуска книги не может быть больше текущего'
CATEGORY_ERROR_MESSAGE = ('при добавлении нового произведения требуется '
                          'указать уже существующую категорию')
GENRE_ERROR_MESSAGE = ('при добавлении нового произведения требуется указать '
                       'уже существующий жанр')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(),
                             many=True)
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    # def validate_year(self, value):
    #     if value > datetime.datetime.now().year:
    #         raise serializers.ValidationError(ERROR_MESSAGE_TITLE)
    #     return value

    def validate(self, data):
        category_slug = data.get('category')
        genre_slugs = data.get('genre')
        year = data.get('year')
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise serializers.ValidationError(CATEGORY_ERROR_MESSAGE)
        genres = []
        for slug in genre_slugs:
            try:
                genre = Genre.objects.get(slug=slug)
                genres.append(genre)
            except Genre.DoesNotExist:
                raise serializers.ValidationError(GENRE_ERROR_MESSAGE)
        if year > datetime.datetime.now().year:
            raise serializers.ValidationError(ERROR_MESSAGE_TITLE)
        data['category'] = category
        data['genre'] = genres
        data['year'] = year
        return data


class GETTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class UserForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для User"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            ),
        )

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me для имени пользователя'
            )
        elif name is None or name == '':
            raise serializers.ValidationError(
                'Требуется ввести имя пользователя'
            )
        return name

    def validate_email(self, email):
        if email is None or email == '':
            raise serializers.ValidationError(
                'Требуется email пользователя'
            )
        return email


class UserForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)

    def validate_username(self, name):
        if not re.fullmatch(PATTERN_USERS, name):
            raise serializers.ValidationError(
                'Имя пользователя не соответствует паттерну'
            )
        return name


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')
