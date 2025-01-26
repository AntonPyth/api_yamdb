from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    # Отображаем поля на странице списка объектов
    list_display = ('name', 'slug')  # какие поля отображать в таблице
    search_fields = ('name', 'slug')  # по каким полям будет работать поиск
    list_filter = ('slug',)  # добавляем фильтрацию по slug
    ordering = ('name',)  # сортируем по полю name
    prepopulated_fields = {'slug': ('name',)}  # автоматически генерировать slug на основе name

    # Можно настроить, какие поля будут отображаться при добавлении или изменении категории
    fields = ('name', 'slug')  # указываем, какие поля показывать в форме
    # Для более сложной настройки формы можно использовать `fieldsets`


# Регистрация модели в админке
admin.site.register(Category, CategoryAdmin)
