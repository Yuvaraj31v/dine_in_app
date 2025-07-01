from rest_framework.exceptions import APIException
from rest_framework import status
from .constants import error_code_dict

class AuthorizationException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = error_code_dict['UNAUTHORIZED_ERROR']['error_code']
    message = error_code_dict['UNAUTHORIZED_ERROR']['error_message']

class UserInactiveException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    code = error_code_dict['INACTIVE_USER']['error_code']
    message = error_code_dict['INACTIVE_USER']['error_message']

class InvalidLoginException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = error_code_dict['INVALID_LOGIN_CREDENTIAL']['error_code']
    message = error_code_dict['INVALID_LOGIN_CREDENTIAL']['error_message']


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = error_code_dict['BAD_REQUEST']['error_code']
    message = error_code_dict['BAD_REQUEST']['error_message']

    def __init__(self,message=None):
        self.message = (message or "")
        super().__init__(detail=self.message)

 

class DatabaseIntegrityException(APIException):
    status_code = status.HTTP_409_CONFLICT
    code = error_code_dict['DATABASE_INTEGRITY']['error_code']
    message = error_code_dict['DATABASE_INTEGRITY']['error_message']

class FieldValidationException(APIException):
    status_code = status.HTTP_409_CONFLICT
    code = error_code_dict['DATABASE_INTEGRITY']['error_code']
    message = error_code_dict['DATABASE_INTEGRITY']['error_message']    

