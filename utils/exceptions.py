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
    default_code = 'bad_request'
    default_detail = 'Bad request.'

    def __init__(self, key=None, message=None):
        if key and key in error_code_dict:
            error_info = error_code_dict[key]
            code = error_info.get('error_code', self.default_code)
            message = message or error_info.get('error_message', self.default_detail)
        else:
            code = self.default_code
            message = message or self.default_detail

        self.code = code
        super().__init__({'code': code, 'message': message})




class DatabaseIntegrityException(APIException):
    status_code = status.HTTP_409_CONFLICT
    code = error_code_dict['DATABASE_INTEGRITY']['error_code']
    message = error_code_dict['DATABASE_INTEGRITY']['error_message']
