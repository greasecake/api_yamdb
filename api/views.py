from .models import Review
from .serializers import ReviewSerializer
from .permissions import (
    AuthorPermisssion,
    AdminPermission,
    ModeratorPermission
)
from rest_framework.viewsets import ModelViewSet


class ReviewViewset(ModelViewSet):
    """
        ТЕСТОВАЯ ВЬЮХА
        Заменить на боевую
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorPermisssion | AdminPermission | ModeratorPermission,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
