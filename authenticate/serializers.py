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
    email = serializers.EmailField(validators=[])
    role = serializers.CharField(validators=[])  

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'role']

    def validate_email(self, value):
        """
        Check if the email already exists and raise a custom error message.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise BadRequestException(key='DUPLICATE_EMAIL')
        return value
    
    def validate_role(self, value):
        """
        Custom validation for the role field.
        - Role must be either manager, customer or admin
        - Role contain only letters
        """
        valid_roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        if value not in valid_roles:
            raise BadRequestException(key='INVALID_ROLE')
        return value

    def validate_name(self, value):
        """
        Custom validation for the name field.
        - Must be at least 3 characters long
        - Must contain only letters and spaces
        """
        if len(value) < 3:
            raise BadRequestException(key='INVALID_USER_NAME')
        
        if not value.replace(" ", "").isalpha():
            raise BadRequestException(key='INVALID_USER_NAME')
        
        return value

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
