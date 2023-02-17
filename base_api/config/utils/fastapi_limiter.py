from math import ceil

from fastapi_helper import DefaultHTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


class RateLimitException(DefaultHTTPException):
    code = "ratelimit"
    type = "TOO_MANY_REQUESTS"
    message = "Too Many Requests"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


async def custom_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)

    raise RateLimitException(message=f"Too Many Requests. Retry-After {str(expire)} secs")