from .views import (
    ReviewViewSet,
    UserMeView,
    UserViewSet,
    get_token,
    get_confirmation
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='Review')
router.register('users', UserViewSet, basename='User')
# router.register('users/me', UserMeView, basename='User')

urlpatterns = [
    path(r'v1/users/me/', UserMeView.as_view(), name='me'),
    path('v1/', include(router.urls)),
]

urlpatterns += [
    path(
        'v1/auth/token/',
        get_token,
        name='get_token'
    ),
    path(
        'v1/auth/email/',
        get_confirmation,
        name='email_confirmation'
    ),
    path(
        'v1/auth/admin_token/',
        TokenObtainPairView.as_view(),
        name='admin_token'
    ),
]
