from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
# (GET, POST) /titles/{title_id}/reviews/
# (GET, PATCH, DELETE) /titles/{title_id}/reviews/{review_id}/
router.register(
    'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
# (GET, POST) /titles/{title_id}/reviews/{review_id}/comments/
# (GET, PATCH, DELETE) /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]