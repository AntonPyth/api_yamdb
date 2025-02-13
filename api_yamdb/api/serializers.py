from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Title, Review
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from .validators import validate_username
from rest_framework.relations import SlugRelatedField


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                "Этот slug уже существует. Выберите другой."
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                "Этот slug уже существует. Выберите другой."
            )
        return value


class SlugJsonRelatedField(serializers.SlugRelatedField):
    def __init__(self, slug_field=None, **kwargs):
        super().__init__(slug_field, **kwargs)

    def to_representation(self, obj):
        return obj.to_json()


class TitleSerializer(serializers.ModelSerializer):
    category = SlugJsonRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    genre = SlugJsonRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'genre',
            'category',
            'year',
            'description',
            'rating'
        )
        model = Title


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs.get("username"))
        if attrs.get("confirmation_code") == str(user.code):
            token = AccessToken.for_user(user)
            return {"token": str(token)}
        raise serializers.ValidationError(
            {"confirmation_code": "Неверный код подтверждения"})


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Этот email уже используется")]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Этот username уже используется"), validate_username]
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class UsersSerializer(UserRegistrationSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UpdateUsersSerializer(UserRegistrationSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        if request is None:
            raise ValidationError('Не удалось получить объект запроса!')
        if request.method != 'POST':
            return attrs
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            not Review.objects
            .filter(title=title, author=request.user)
            .exists()
        ):
            return attrs
        raise ValidationError('Может существовать только один отзыв!')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
