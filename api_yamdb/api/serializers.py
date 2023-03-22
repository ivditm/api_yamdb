from django.shortcuts import get_object_or_404
import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

import datetime

from reviews.models import Review, User, Genre, Category, Title, Comment

ERROR_MESSAGE_TITLE = 'год выпуска книги не может быть больше текущего'


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class CategoryTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class GenreTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryTitle(slug_field='slug',
                             queryset=Category.objects.all(),
                             required=False)
    genre = GenreTitle(slug_field='slug',
                       queryset=Genre.objects.all(),
                       many=True)
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


class UserForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)


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
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Недопустимое значение!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review', 'pub_date')
