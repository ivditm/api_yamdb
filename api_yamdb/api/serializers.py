from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

import datetime


from reviews.models import Genre, Category, Title


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
