from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
]
