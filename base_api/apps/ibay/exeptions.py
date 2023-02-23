from fastapi_helper import DefaultHTTPException
from starlette import status


class WalletIsUndefined(DefaultHTTPException):
    code = "Wallet undefined"
    type = "Wallet invalid"
    message = "This wallet is undefined"
    status_code = status.HTTP_400_BAD_REQUEST


class ProductDoesNotExistsOrAlreadySold(DefaultHTTPException):
    code = "Product undefined"
    type = "Product invalid"
    message = "This product does not exist or sold already"
    status_code = status.HTTP_400_BAD_REQUEST


class TheSameWalletError(DefaultHTTPException):
    code = "Wallet error"
    type = "Wallet invalid"
    message = "You can buy your own product with the same wallet. Please choose another wallet"
    status_code = status.HTTP_400_BAD_REQUEST
