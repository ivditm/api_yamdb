import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

import datetime


from reviews.models import User, Genre, Category, Title, Review

PATTERN_USERS = re.compile(r'[\\w.@+-]+\\z')
ERROR_MESSAGE_TITLE = 'год выпуска книги не может быть больше текущего'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


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

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(ERROR_MESSAGE_TITLE)
        return value


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title', 'pub_date')
    
    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Значение должно быть в диапазоне от 1 до 10!'
            )
        return value
