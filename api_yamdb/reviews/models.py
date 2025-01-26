from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


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


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
        blank=False
    )
    year = models.PositiveIntegerField(
        verbose_name="Год создания",
        blank=False
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
        related_name='titles',
        verbose_name="Категория"
    )

    description = models.TextField(  # Новое поле description
        verbose_name="Описание произведения",
        blank=True,  # Позволяет оставлять поле пустым
        null=True  # Позволяет сохранить NULL, если описание отсутствует
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
        related_name='genre_titles',
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


    '''description = models.TextField(blank=True, verbose_name="Описание")
    rating = models.PositiveIntegerField(
        default=0,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )'''


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
