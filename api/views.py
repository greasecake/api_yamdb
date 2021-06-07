import binascii
import os

from django_filters.rest_framework.backends import DjangoFilterBackend

from .models import (
    Review,
    Confirmation,
    Review,
    Title,
    Category,
    Genre
)
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    TokenSerializer,
    WriteTitleSerializer,
    ReadTitleSerializer,
    CategorySerializer,
    GenreSerializer
)
from .permissions import (
    AuthorPermisssion,
    AdminPermission,
    AdminOrReadOnly,
    ModeratorPermission
)
from .paginations import StandardResultsSetPagination
from .filters import TitleFilterSet
from .viewsets import CustomModelViewSet

from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Работа с отзывами на произведения
    """
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
        if Review.objects.filter(
                title=title, author=self.request.user).exists():
            raise ValidationError(
                'Вы уже публиковали отзыв на это произведение.'
            )
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Работа с комментариями к отзывам.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorPermisssion | AdminPermission | ModeratorPermission,
    )
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):

        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'


class UserMeView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, username=user)
        return obj


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(request.data)
    email = serializer.data['email']
    confirmation = serializer.data['confirmation']
    key = get_object_or_404(Confirmation, email=email).key
    if confirmation == key:
        user = User.objects.create(
            username=email,
            email=email,
            role='user'
        )
        user.save()
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)})
    return Response('Something is wrong')


@api_view(['POST'])
def get_confirmation(request):
    serializer = TokenSerializer(request.data)
    key = binascii.hexlify(os.urandom(20)).decode()
    email = serializer.data['email']
    Confirmation.objects.update_or_create(
        email=email,
        defaults={
            'email': email,
            'key': key
        }
    )
    send_mail(
        subject='Confirmation',
        message=key,
        from_email='admin@yamdb.fake',
        recipient_list=[email]
    )
    return Response({
        'confirmation': key
    })


class CategoryViewSet(CustomModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return WriteTitleSerializer
        return ReadTitleSerializer


class GenreViewSet(CustomModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
