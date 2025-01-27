import random
from django.core.mail import send_mail
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet
from .common import send_verification_email, generate_verification_code

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [path('', include(router.urls)),]


