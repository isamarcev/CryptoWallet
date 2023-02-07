from fastapi_helper import DefaultHTTPException
from starlette import status


class WalletCreatingError(DefaultHTTPException):
    code = "Privet key error"
    type = "Privet Key Invalid"
    message = "Server can't create wallet"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidWalletImport(DefaultHTTPException):
    code = "Privet key error"
    type = "Privet Key Invalid"
    message = "Privet Key Invalid"
    status_code = status.HTTP_400_BAD_REQUEST


class WalletAlreadyExists(DefaultHTTPException):
    code = "Wallet already exists"
    type = "Wallet invalid"
    message = "This wallet is already exists"
    status_code = status.HTTP_400_BAD_REQUEST


class WalletIsNotDefine(DefaultHTTPException):
    code = "Wallet is not defined"
    type = "Wallet invalid"
    message = "This wallet is not defined"
    status_code = status.HTTP_400_BAD_REQUEST

