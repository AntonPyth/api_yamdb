from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import json


def validate_year(value):
    current_year = now().year
    if value > current_year:
        raise ValidationError(
            f'Год не может быть больше текущего ({current_year}).'
        )


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
        blank=False
    )
    slug = models.SlugField(max_length=50, unique=True, blank=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=["slug"]),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name

    def to_json(self):
        return json.loads(f'{{"name": "{self.name}", "slug": "{self.slug}"}}')


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
        blank=False
    )
    slug = models.SlugField(max_length=50, unique=True, blank=False)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        indexes = [
            models.Index(fields=["slug"]),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name

    def to_json(self):
        return json.loads(f'{{"name": "{self.name}", "slug": "{self.slug}"}}')


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
        blank=False
    )
    year = models.PositiveIntegerField(
        verbose_name="Год создания",
        blank=False,
        validators=[validate_year]
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Title',
        verbose_name="Категория"
    )

    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "Title"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def rating(self):
        return (
            self.reviews.aggregate(average_score=Avg('score'))['average_score']
        )


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name="Название произведения"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='genre_title',
        verbose_name="Жанр произведения"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre',
            ),
        ]

    def __str__(self):
        return f"Произведение {self.title} относится к жанру {self.genre}"


class ReviewsUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    code = models.TextField(blank=True, verbose_name='Код')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_user(self):
        return self.role == self.Role.USER


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        ReviewsUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст отзыва', blank=False)
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_author'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.score} от {self.author} на {self.title}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        ReviewsUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария', blank=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return f'Комментарий от {self.author} к отзыву {self.review}'
