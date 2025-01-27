
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .filters import TitlesFilter
from reviews.models import Category, Genre, Titles
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer
from .utils import send_verification_email, generate_verification_code
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters, viewsets, mixins
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly, IsAdmin
from .serializers import (
    UserRegistrationSerializer, UsersSerializer,
    UpdateUsersSerializer, TokenSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        slug = request.data.get('slug')

        # Проверка на отсутствие обязательных полей
        if not name or not slug:
            raise ValidationError(
                {'detail': 'Поле `name` и `slug` обязательны.'})

        # Проверка на уникальность slug
        if Category.objects.filter(slug=slug).exists():
            raise ValidationError(
                {'slug': 'Этот slug уже существует. Выберите другой.'})

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class GenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        slug = request.data.get('slug')

        # Проверка на отсутствие обязательных полей
        if not name or not slug:
            raise ValidationError(
                {'detail': 'Поле `name` и `slug` обязательны.'})

        # Проверка на уникальность slug
        if Category.objects.filter(slug=slug).exists():
            raise ValidationError(
                {'slug': 'Этот slug уже существует. Выберите другой.'})

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class TitlesViewSet(ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        year = request.data.get('year')
        genre = request.data.get('genre')
        category = request.data.get('category')

        # Проверка на заполнение обязательных полей
        if not name or not year or not genre or not category:
            raise ValidationError(
                {'detail': 'Поля `name`, `year`, `genre` и `category` являются обязательными.'}
            )

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        """Disallow full update (PUT) and allow partial update (PATCH)."""
        if kwargs.get("partial", False):  # Use .get() instead of .pop()
            return super().update(request, *args, **kwargs)

        raise MethodNotAllowed(request.method)


User = get_user_model()


class UserRegistrationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        result = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if not result:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            result.code = generate_verification_code()
            result.save()
        send_verification_email(result, result.code)
        return Response(
            {'username': result.username, 'email': result.email},
            status=status.HTTP_200_OK
        )


class UserVerificationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = TokenSerializer

    def perform_create(self, serializer):
        return Response(serializer.validated_data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False, methods=['get'], url_path='me',
        permission_classes=[IsAuthenticated])
    def user_information(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @user_information.mapping.patch
    def user_update(self, request):
        serializer = UpdateUsersSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
