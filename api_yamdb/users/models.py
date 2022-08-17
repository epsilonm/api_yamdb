from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=154,
        validators=[validate_username],
        unique=True
    )
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=150,
        blank=True
    )
    role = models.CharField(max_length=9,
                            choices=settings.USER_ROLES,
                            default='user')
    password = models.CharField(
        verbose_name='Password',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['email']
