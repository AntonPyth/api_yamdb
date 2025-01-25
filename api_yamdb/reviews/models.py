from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название категории"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=["slug"]),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название жанра"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        indexes = [
            models.Index(fields=["slug"]),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название произведения"
    )
    year = models.PositiveIntegerField(
        verbose_name="Год создания"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        # При удалении объекта произведения Title должны удаляться
        # Все отзывы к этому произведению и комментарии к ним.
        # Использует on_delete=models.SET_NULL,
        # Чтобы при удалении категории у произведения значение категории
        # Становилось NULL, а не удалялось произведение.
        null=True,
        blank=True,
        related_name='categorie',
        verbose_name="Категория"
    )
    '''description = models.TextField(blank=True, verbose_name="Описание")
    rating = models.PositiveIntegerField(
        default=0,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )'''

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name="Название произведения"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        # При удалении объекта жанра (Genre) не нужно удалять
        # Связанные с этим жанром произведения.
        null=True,
        blank=True,
        related_name='genre',
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
