from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet, CategoryViewSet, GenreViewSet
)


router = DefaultRouter()
router.register(r'^categories', CategoryViewSet)
router.register(r'^genres', GenreViewSet)
router.register(r'^titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
