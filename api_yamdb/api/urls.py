from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet, ReviewViewSet, CommentViewSet)


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='Title')
router.register('users', UsersViewSet, basename='users')
router.register('auth/token', UserVerificationViewSet, basename='token')
router.register(
    'auth/signup', UserRegistrationViewSet, basename='registration')
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(router.urls)),
]
