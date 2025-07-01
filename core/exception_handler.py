import logging

from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status


# Use root logger
logger = logging.getLogger()

def handle_exceptions(exc, context):
    """
    Custom exception handler that transforms DRF's default error
    response into a consistent JSON format for APIExceptions.

    Parameters:
        exc (Exception): The exception that was raised.
        context (dict): Context about the request being handled.

    Returns:
        Response: A DRF Response object with custom JSON structure.
    """
    # Let DRF handle the exception first
    output_response = exception_handler(exc, context)

    # Add custom handling for JWT exceptions
    if isinstance(exc, (InvalidToken, TokenError)):
        return Response({
            'detail': 'Token is invalid or expired.',
            'error_code': 'token_not_valid'
        }, status=status.HTTP_401_UNAUTHORIZED)

    if output_response is not None and isinstance(exc, APIException):
        logger.warning("Handled APIException: code=%s, message=%s", getattr(exc, 'code', None), getattr(exc, 'message', str(exc.detail)))
        return Response({
            'code': getattr(exc, 'code', 'UNKNOWN_ERROR'),
            'message': getattr(exc, 'message', str(exc.detail))
        }, status=exc.status_code)

    # Log unexpected/unhandled exceptions
    logger.error("Unhandled exception: %s | Context: %s", str(exc), context)

    return output_response