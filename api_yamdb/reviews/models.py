from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )