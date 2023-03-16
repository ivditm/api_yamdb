from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, ReviewViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/', include(router_v1.urls)),
]
