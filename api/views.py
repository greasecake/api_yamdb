import binascii
import os

from .models import (
    Review,
    Confirmation,
    Review,
    Title,
)
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    TokenSerializer,
)
from .permissions import (
    AuthorPermisssion,
    AdminPermission,
    AdminOrReadOnly,
    ModeratorPermission
)
from .paginations import StandardResultsSetPagination

from rest_framework import viewsets, filters, status, response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer
)
from .models import Title, Category, Genre


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
        serializer.save(author=self.request.user, title=title)


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


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, slug=pk)
        self.perform_destroy(category)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)

    def destroy(self, request, pk=None):
        genre = get_object_or_404(Genre, slug=pk)
        self.perform_destroy(genre)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
