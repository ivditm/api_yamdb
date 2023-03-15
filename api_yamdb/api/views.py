from django.shortcuts import get_object_or_404, render
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reviews.models import User, Category, Genre,  Title

from .permissions import IsAdminPermission
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          UserForAdminSerializer,
                          UserForUserSerializer)


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