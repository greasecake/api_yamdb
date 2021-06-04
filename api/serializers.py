from .models import Review
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    Serializer,
    EmailField,
    CharField
)
from django.contrib.auth import get_user_model


User = get_user_model()


class ReviewSerializer(ModelSerializer):
    """
        ТЕСТОВЫЙ СЕРИАЛИЗАТОР
        Заменить на боевой
    """
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ['author']
        model = Review


class UserSerializer(ModelSerializer):
    class Meta:
        fields = [
            'username',
            'email',
            'bio',
            'role',
            'first_name',
            'last_name'
        ]
        model = User


class TokenSerializer(Serializer):
    email = EmailField()
    confirmation = CharField(max_length=20)


class ConfirmationSerializer(Serializer):
    email = EmailField()
