from rest_framework import serializers
from reviews.models import Category, Genre, Title
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
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


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
