from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


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
    description = models.CharField(
        blank=True,
        max_length=100
    )

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
    # id
    # title_id объект для оценки
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    # string (Текст отзыва)
    text = models.CharField(
        "Текст отзыва",
        max_length=1500,
        help_text='Максимальная длина 1500 символов'
    )
    # string (username пользователя)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='author',
    )
    # integer (Оценка) [ 1 .. 10 ]
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    # string <date-time> (Дата публикации отзыва)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    # id (comment_id) integer (ID комментария)
    # review_id  ID отзыва
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    # string (Текст комментария)
    text = models.CharField(
        "Текст комментария",
        max_length=1500,
        help_text='Максимальная длина 1500 символов'
    )
    # string (username автора комментария)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='author',
    )
    # string <date-time> (Дата публикации комментария)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
