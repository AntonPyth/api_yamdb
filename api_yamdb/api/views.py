from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import CategoryGenreMixin
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomTokenObtainSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializerNonSafe,
                          TitleSerializerSafe, UserSerializer,
                          UserSignUpSerializer)

User = get_user_model()

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для управления отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        title_object = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title_object)

