from fastapi_helper import DefaultHTTPException
from starlette import status


class UndefinedUser(DefaultHTTPException):
    code = "user_undefined"
    type = "User Invalid"
    message = "User is not defined"
    status_code = status.HTTP_401_UNAUTHORIZED


class MessageForbidden(DefaultHTTPException):
    code = "User forbidden"
    type = "User Forbidden"
    message = "User can't send message"
    status_code = status.HTTP_403_FORBIDDEN
