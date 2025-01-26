from .views import CategoryViewSet, GenreViewSet, TitlesViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'auth/token', UserVerificationViewSet, basename='token')
router.register(
    r'auth/signup', UserRegistrationViewSet, basename='registration')
urlpatterns = [
    path('v1/', include(router.urls)),
]
