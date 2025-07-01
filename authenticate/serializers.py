from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from utils.exceptions import (
    InvalidLoginException,
    UserInactiveException,
    BadRequestException,
    DatabaseIntegrityException,
)

class LoginSerializers(serializers.Serializer):
    """
    Serializer for handling user login input and JWT generation.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    def validate(self, data):
        """
        Validates user credentials and returns tokens if valid.
        Raises custom exceptions for invalid or inactive users.
        """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise InvalidLoginException()

        if not user.status:
            raise UserInactiveException()

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'email': user.email,
            'name': user.name,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'last_login': user.last_login,
        }

class RegisterSerializers(serializers.ModelSerializer):
    """
    Serializer for handling user registration input and creation.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'role']

    def create(self, validated_data):
        """
        Creates a new user. Raises custom exceptions on DB or logic errors.
        """
        email = validated_data.get('email')
        try:
            user = CustomUser.objects.create_user(**validated_data)
            return user
        except IntegrityError as e:
            raise DatabaseIntegrityException()
        except Exception as e:
            raise BadRequestException()


class UserSerializer(serializers.ModelSerializer):
    """
    Simple serializer for returning user details.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name']
