from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from uuid import uuid4

from .filters import TitleFilter
from .permissions import (IsAdminPermission, IsAdminOrReadOnly,
                          IsAuthorOrReadOnlyPermission)
from reviews.models import Category, Genre, Title, User, Review
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer,
                          UserForAdminSerializer, UserForUserSerializer,
                          ReviewSerializer, CommentSerializer,
                          GetTokenSerializer, SignupSerializer)

DEFAULT_EMAIL_SUBJECT = 'Подтверждение регистрации пользователя'
DEFAULT_FROM_EMAIL = 'message@yamdb.com'


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомный вьюсет."""
    pass


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)


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


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    confirmation_code = str(uuid4)
    username = request.data.get('username')
    email = request.data.get('email')
    user = User.objects.filter(username=username, email=email)
    if (
        User.objects.filter(username=username).exists()
        and User.objects.get(username=username).email == email
    ):
        send_mail(
            subject=DEFAULT_EMAIL_SUBJECT,
            message=confirmation_code,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=(user[0].email,)
        )
        return Response(request.data, status=status.HTTP_200_OK)
    elif (
        User.objects.filter(username=username).exists()
        and User.objects.get(username=username).email != email
    ):
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    elif (
        User.objects.filter(email=email).exists()
        and User.objects.get(email=email).username != username
    ):
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, _ = User.objects.get_or_create(
            username=username, email=email,
            confirmation_code=confirmation_code
        )
        send_mail(
            subject=DEFAULT_EMAIL_SUBJECT,
            message=confirmation_code,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(
        User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    @property
    def __title_if_exist(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )

    def get_queryset(self):
        return self.__title_if_exist.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.__title_if_exist
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    @property
    def __review_if_exist(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id")
        )

    def get_queryset(self):
        return self.__review_if_exist.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.__review_if_exist
        )
