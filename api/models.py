from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    # review_id
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
        related_name='reviews'
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
