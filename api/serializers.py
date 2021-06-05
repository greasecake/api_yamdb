from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Title, Genre, Review


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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('category', instance.category)
        instance.genre.set(validated_data.get('genre', instance.genre))
        return instance

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.id).aggregate(
            Avg('score')).get('score__avg')
        if rating is None:
            return 'None'
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
