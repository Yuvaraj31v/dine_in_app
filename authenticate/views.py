import logging

from django.utils import timezone  # Django framework (major)

from rest_framework import status  # third-party Django add-ons
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializers, RegisterSerializers, UserSerializer  # local app
from utils.exceptions import AuthorizationException, BadRequestException
from core.logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handles user login, validates credentials,
    and returns JWT access and refresh tokens.
    """
    serializer = LoginSerializers(data=request.data)
    logger.warning("Food view triggered")
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Update user's last login time
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        # Serialize user data for response
        user_data = UserSerializer(user).data
        return Response({
            'user': user_data,
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
        })

    # Raise custom exception on failed login
    raise AuthorizationException()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Handles user registration and returns basic user info.
    """
    serializer = RegisterSerializers(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'email': user.email,
            'name': user.name
        }, status=status.HTTP_201_CREATED)

    # Raise custom exception on validation failure
    raise BadRequestException(str(serializer.errors))
