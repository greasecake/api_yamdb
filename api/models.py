from django.db import models
from django.contrib.auth.models import AbstractUser
# from rest_framework.authtoken.models import Token


class Confirmation(models.Model):
    key = models.CharField(max_length=20)
    email = models.EmailField()


class User(AbstractUser):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (MODER, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    role = models.TextField(
        blank=True,
        choices=ROLES,
    )
    bio = models.CharField(
        blank=True,
        max_length=100
    )
    description = models.CharField(
        blank=True,
        max_length=100
    )
    email = models.EmailField(unique=True)

    @property
    def is_admin(self):
        return bool(
            self.role == self.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == self.MODER


class Title(models.Model):
    """
        ТЕСТОВАЯ МОДЕЛЬ
        Заменить на боевую
    """
    name = models.TextField()


class Review(models.Model):
    """
        ТЕСТОВАЯ МОДЕЛЬ
        Заменить на боевую
    """
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
