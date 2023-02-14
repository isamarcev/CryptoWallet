from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import as_form, ApiSchema
from pydantic import BaseModel, validator
from web3 import Web3


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
    address: str
    price: float
    image: str

    class Config:
        orm_mode = True


class Wallet(ApiSchema):
    public_key: str

    class Config:
        orm_mode = True


class Products(BaseModel):
    title: str
    price: float
    image: str
    wallet: Wallet

    class Config:
        orm_mode = True
