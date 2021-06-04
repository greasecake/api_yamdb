from .models import Review
from .models import Comment, Review

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class UserSerializer(serializers.ModelSerializer):
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


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation = serializers.CharField(max_length=20)


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
