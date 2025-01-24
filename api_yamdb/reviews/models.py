from datetime import date
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import PastOrPresentYearValidator


User = get_user_model()

DEFAULT_SINT = 0
MAX_LENGTH_CHAR = 256


class Comment(models.Model):
    """Комментарии к отзывам."""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class Review(models.Model):
    """Отзывы."""

    text = models.TextField()
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]

    def __str__(self):
        return self.text
