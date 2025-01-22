from django.contrib.auth.models import AbstractUser
from django.db import models


class ReviewsUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=254,
        unique=True,
        verbose_name='Логин'
    )
    first_name = models.CharField(
        max_length=254,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=254,
        blank=True,
        verbose_name='Фамилия'
    )

    role = models.CharField(
        max_length=254,
        choices=(
            (USER, 'user'),
            (MODERATOR, 'moderator'),
            (ADMIN, 'admin'),
        ),
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
