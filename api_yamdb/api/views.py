from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .filters import TitleFilter
from permissions import IsAdminPermission
from reviews.models import Category, Genre, Title, User
from .serializers import (CategorySerializer, GenreSerializer,
                          GETTitleSerializer, TitleSerializer,
                          UserForAdminSerializer, UserForUserSerializer)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = ('username')
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def users_profile(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserForUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
