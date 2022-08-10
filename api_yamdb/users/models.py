from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    username = models.CharField(
        verbose_name='Username',
        unique=True,
        max_length=150,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=150,
    )
    role = models.CharField(max_length=9,
                            choices=USER_ROLES,
                            default='user')
    is_active = True
    confirmation_code = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['email']
