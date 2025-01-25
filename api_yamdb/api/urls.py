
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),

v1_router = DefaultRouter()
v1_router.register(r'users', UsersViewSet, basename='users')
v1_router.register(r'auth/token', UserVerificationViewSet, basename='token')
v1_router.register(
    r'auth/signup', UserRegistrationViewSet, basename='registration')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
