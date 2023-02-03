from fastapi_helper import DefaultHTTPException
from starlette import status


class UndefinedUser(DefaultHTTPException):
    code = "user_undefined"
    type = "User Invalid"
    message = "User is not defined"
    status_code = status.HTTP_401_UNAUTHORIZED
