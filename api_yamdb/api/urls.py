from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet, ReviewViewSet, CommentViewSet)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='Title')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'auth/token', UserVerificationViewSet, basename='token')
router.register(
    r'auth/signup', UserRegistrationViewSet, basename='registration')
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
