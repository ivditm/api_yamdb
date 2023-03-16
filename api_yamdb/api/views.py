from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets


from permissions import IsAdminPermission
from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          GETTitleSerializer, TitleSerializer)
from .filters import TitleFilter


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомный вьюсет."""
    pass


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (TitleFilter,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GETTitleSerializer
        return TitleSerializer

    def annotate_queryset(self, queryset):
        return queryset.annotate(avg_rating=Avg('rating'))

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.annotate_queryset(queryset)
