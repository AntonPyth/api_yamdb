from rest_framework import serializers
from reviews.models import Category, Genre, Titles, Genre_title
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from .validators import validate_username


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


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=False
    )
    genre = GenreSerializer(required=False, many=True)

    class Meta:
        fields = ('id', 'name', 'genre', 'category', 'year')
        model = Titles

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Titles.objects.create(**validated_data)
            return title
        else:
            genre = validated_data.pop('genre')
            title = Titles.objects.create(**validated_data)
            for one_genre in genre:
                current_genre, status = Genre.objects.get_or_create(
                    **one_genre
                )
                Genre_title.objects.create(genre=current_genre, title=title)
            return title


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
        max_length=254,
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
