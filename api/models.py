from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    Ресурс REVIEWS: отзывы на произведения.
    Отзыв привязан к определённому произведению.

    Parameters
    ----------
    title : Title
        Объект для оценки
    text : string
        Текст отзыва
    author : User
        Пользователя
    score : Int
        Оценка от 1 до 10
    pub_date : DateTime
        Дата публикации отзыва
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.CharField(
        "Текст отзыва",
        max_length=1500,
        help_text='Максимальная длина 1500 символов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='author',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        "Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[:40] + '...'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    """
    Ресурс COMMENTS: комментарии к отзывам.
    Комментарий привязан к определённому отзыву.

    Parameters
    ----------
    review : Review
        Объект отзыва
    text : string
        Текст комментария
    author : User
        Автор комментария
    pub_date : DateTime
        Дата публикации комментария
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.CharField(
        "Текст комментария",
        max_length=1500,
        help_text='Максимальная длина 1500 символов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='author',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[:40] + '...'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
