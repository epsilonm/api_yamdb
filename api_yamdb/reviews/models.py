from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,   
        verbose_name='Название'
    )


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
