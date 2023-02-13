from fastapi_helper import DefaultHTTPException
from starlette import status


class WalletIsUndefined(DefaultHTTPException):
    code = "Wallet undefined"
    type = "Wallet invalid"
    message = "This wallet is undefined"
    status_code = status.HTTP_400_BAD_REQUEST
