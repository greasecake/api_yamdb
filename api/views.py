from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .models import Review, Comment, Title, User
from .paginations import StandardResultsSetPagination
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import (
    AuthorPermisssion,
    AdminPermission,
    ModeratorPermission
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorPermisssion | AdminPermission | ModeratorPermission,
    )
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    #permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
