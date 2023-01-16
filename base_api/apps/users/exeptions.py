from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class InvalidEmail(DefaultHTTPException):
    code = "invalid email"
    status_code = status.HTTP_400_BAD_REQUEST
    # message =