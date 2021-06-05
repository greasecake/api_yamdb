from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=20,
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        unique=True
    )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=20,
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        unique=True
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=100,
    )
    year = models.IntegerField(verbose_name='Год создания')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        db_table='api_genre_title',
        verbose_name='Жанры произведения'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
        null=False,
        default=''
    )


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_column='title_id'
    )
    score = models.IntegerField(default=0)
