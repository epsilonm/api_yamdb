from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from users.validators import validate_username

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
<<<<<<< HEAD
        verbose_name='Username',
=======
        verbose_name='Имя пользователя',
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
        max_length=154,
        validators=[validate_username],
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
<<<<<<< HEAD
        verbose_name='First name',
=======
        verbose_name='Имя',
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
<<<<<<< HEAD
        verbose_name='Last name',
=======
        verbose_name='Фамилия',
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
        max_length=150,
        blank=True
    )
    role = models.CharField(max_length=9,
                            choices=settings.USER_ROLES,
                            default='user')
    password = models.CharField(
<<<<<<< HEAD
        verbose_name='Password',
=======
        verbose_name='Пароль',
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['email']
<<<<<<< HEAD



=======
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
