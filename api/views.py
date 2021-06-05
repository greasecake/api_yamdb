from rest_framework import viewsets, filters, status, response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer
)
from .models import Title, Category, Genre


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    # permission_classes

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


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    # permission_classes

    def destroy(self, request, pk=None):
        genre = get_object_or_404(Genre, slug=pk)
        self.perform_destroy(genre)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
