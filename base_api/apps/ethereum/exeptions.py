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
    message = "Server can't import wallet"
    status_code = status.HTTP_400_BAD_REQUEST
