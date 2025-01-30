from django.contrib import admin
from .models import (
    Category, Comment, Genre, GenreTitle,
    ReviewsUser, Review, Title
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'rating')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    ordering = ('name',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    search_fields = ('title__name', 'genre__name')


@admin.register(ReviewsUser)
class ReviewsUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role',
                    'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser')
    ordering = ('username',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('title__name', 'author__username', 'text')
    list_filter = ('score', 'pub_date')
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date')
    search_fields = ('review__text', 'author__username', 'text')
    list_filter = ('pub_date',)
    ordering = ('pub_date',)
