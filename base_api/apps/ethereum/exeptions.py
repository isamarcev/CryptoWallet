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
    field = "from_address"
    status_code = status.HTTP_400_BAD_REQUEST


class Web3ConnectionError(DefaultHTTPException):
    code = "Web3 error"
    type = "Web3 invalid"
    message = "Problem with connection to Web3, please try again later"
    status_code = status.HTTP_400_BAD_REQUEST


class TransactionError(DefaultHTTPException):
    code = "Transaction error"
    type = "Transaction invalid"
    message = "Create transaction error"
    status_code = status.HTTP_400_BAD_REQUEST


class WalletAddressError(DefaultHTTPException):
    code = "Address error"
    type = "Address invalid"
    message = "Wallet address is invalid"
    status_code = status.HTTP_400_BAD_REQUEST
