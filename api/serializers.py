from .models import (
    Comment,
    Review,
    Category,
    Title,
    Genre,
    Review
)

from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth import get_user_model


User = get_user_model()


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category'
        )
        model = Title

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        instance = Title.objects.create(**validated_data)
        instance.genre.set(genre)
        return instance

    def partial_update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        if not validated_data.get('genre', None) is None:
            instance.category = Category.objects.get(
                slug=validated_data.get('category')
            )
        if not validated_data.get('genre', None) is None:
            instance.genre.set(validated_data.get('genre'))
        return instance

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.id).aggregate(
            Avg('score')).get('score__avg')
        if rating is None:
            return None
        return round(rating, 1)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            Category.objects.get(slug=representation.pop('category'))
        ).data
        representation['genre'] = GenreSerializer(
            Genre.objects.filter(slug__in=representation.pop('genre')),
            many=True
        ).data
        return representation
