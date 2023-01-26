from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


# class InvalidEmail(DefaultHTTPException):
#     code = "invalid email"
#     status_code = status.HTTP_400_BAD_REQUEST
#     # message =


class UsernameInvalidException(DefaultHTTPException):
    code = "username_error"
    type = "Username Invalid"
    message = "Username must contain at least: 5 to 40 characters, not special characters"
    status_code = status.HTTP_400_BAD_REQUEST