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
        on_delete=models.CASCADE,
        related_name='categorie',
        verbose_name="Категория"
    )

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
        on_delete=models.CASCADE,
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
        return f"{self.title} имеет {self.genre}"
