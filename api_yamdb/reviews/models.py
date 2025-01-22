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
