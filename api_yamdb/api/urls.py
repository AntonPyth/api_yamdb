from .views import CategoryViewSet, GenreViewSet, TitlesViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet)


v1_router = DefaultRouter()
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitlesViewSet, basename='titles')
v1_router.register(r'users', UsersViewSet, basename='users')
v1_router.register(r'auth/token', UserVerificationViewSet, basename='token')
v1_router.register(
    r'auth/signup', UserRegistrationViewSet, basename='registration')
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
