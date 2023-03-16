from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet


router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/', include(router_v1.urls)),
]
