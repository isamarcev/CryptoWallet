from enum import Enum
from typing import Union

from pydantic import BaseModel, validator
from pydantic.types import UUID
from datetime import datetime
from web3 import Web3


class WalletCreate(BaseModel):
    public_key: str
    privet_key: str
    user: UUID

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class WalletDetail(BaseModel):
    public_key: str
    user: UUID

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class WalletImport(BaseModel):
    privet_key: str

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class StatusEnum(str, Enum):
    success = 'Success'
    pending = 'Pending'
    failed = 'Failed'


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')


class WalletTransactions(BaseModel):
    number: str
    from_address: str
    to_address: str
    value: float
    date: datetime
    txn_fee: Union[None, str]
    status: StatusEnum

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class WalletsInfo(BaseModel):
    public_key: str
    balance: float
    # transactions: List[WalletTransactions] = []

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class CreateTransaction(BaseModel):
    from_address: str
    to_address: str
    amount: float

    class Config:
        orm_mode = True


class CreateTransactionReceipt(BaseModel):
    number: str
    from_address: str
    to_address: str
    value: float
    date: datetime
    txn_fee: Union[None, str]
    status: StatusEnum
    wallet: str

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class TransactionURL(BaseModel):
    url: str

    class Config:
        orm_mode = True


class GetTransactions(BaseModel):
    wallet: str

    @validator("wallet", pre=True)
    def name_must_be_more_than_five(cls, wallet):
        if Web3.isAddress(wallet):
            return wallet
        raise ValueError("Not valid wallet address")

    class Config:
        orm_mode = True


