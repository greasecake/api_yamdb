from .models import Review
from rest_framework.serializers import ModelSerializer, SlugRelatedField


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
