from typing import Union
from uuid import UUID

from datetime import datetime
from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import as_form, ApiSchema
from pydantic import BaseModel, validator
from web3 import Web3

from base_api.apps.ibay.enums import OrderStatus

def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')


@as_form
class CreateProduct(BaseModel):
    title: str
    address: str
    price: float
    image: UploadFile

    @validator("address", pre=True)
    def name_must_be_more_than_five(cls, address):
        if Web3.isAddress(address):
            return address
        raise ValueError("Not valid wallet address")


class ProductInfo(BaseModel):
    title: str
    address: UUID
    price: float
    image: str

    class Config:
        orm_mode = True


class Wallet(ApiSchema):
    public_key: str

    class Config:
        orm_mode = True


class Products(BaseModel):
    id: UUID
    title: str
    price: float
    image: str
    wallet: Wallet

    class Config:
        orm_mode = True


class Orders(BaseModel):
    id: UUID
    txn_hash: str
    datetime: datetime
    status: OrderStatus
    txn_hash_return: Union[str, None]
    product: ProductInfo

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
        orm_mode = True


class CreateOrder(BaseModel):
    product_id: str
    from_wallet: str

    class Config:
        orm_mode = True

    @validator("from_wallet")
    def is_wallet_address(cls, from_wallet):
        if Web3.isAddress(from_wallet):
            return from_wallet
        raise ValueError("Not valid wallet address")

