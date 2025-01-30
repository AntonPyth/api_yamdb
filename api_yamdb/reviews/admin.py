# from django.contrib import admin 
# from .models import ( 
#     Category, Genre, 
#     Title, Genre_title, 
#     ReviewsUser, Review, Comment 
# ) 
 
 
# class CategoryAdmin(admin.ModelAdmin): 
#     # Отображаем поля на странице списка объектов 
#     list_display = ('name', 'slug')  # какие поля отображать в таблице 
#     # по каким полям будет работать поиск 
#     search_fields = ('name', 'slug') 
#     list_filter = ('slug',)  # добавляем фильтрацию по slug 
#     ordering = ('name',)  # сортируем по полю name 
#     # автоматически генерировать slug на основе name 
#     prepopulated_fields = {'slug': ('name',)} 
 
#     # Можно настроить, какие поля будут отображаться 
#     # при добавлении или изменении категории 
#     # указываем, какие поля показывать в форме 
#     fields = ('name', 'slug') 
#     # Для более сложной настройки формы можно использовать `fieldsets` 
 
 
# # Регистрация модели в админке 
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Genre) 
# admin.site.register(Title) 
# admin.site.register(Genre_title) 
# admin.site.register(ReviewsUser) 
# admin.site.register(Review) 
# admin.site.register(Comment) 
 



from django.contrib import admin
from django.contrib.admin import AdminSite
from .admin import CategoryAdmin
from .models import (
    Category, Genre,
    Title, GenreTitle,
    ReviewsUser, Review, Comment
)



def register(model_class, admin_class):
    def decorator(admin_site):
        admin_site.register(model_class, admin_class)
        return admin_site
    return decorator

@register(Category, CategoryAdmin)
@register(Genre, admin.ModelAdmin)
@register(Title, admin.ModelAdmin)
@register(GenreTitle, admin.ModelAdmin)
@register(ReviewsUser, admin.ModelAdmin)
@register(Review, admin.ModelAdmin)
@register(Comment, admin.ModelAdmin)


class MyAdminSite(AdminSite):
    site_header = "Мой админ"
    site_title = "Админка"
    index_title = "Управление"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug')
