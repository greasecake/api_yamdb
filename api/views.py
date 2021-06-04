import binascii
import os

from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review, Confirmation
from .serializers import (
    ReviewSerializer,
    UserSerializer,
    TokenSerializer
)
from .permissions import (
    AuthorPermisssion,
    AdminPermission,
    ModeratorPermission
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class ReviewViewSet(ModelViewSet):
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


class UserViewSet(ModelViewSet):
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
