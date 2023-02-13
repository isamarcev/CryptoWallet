from pydantic import BaseModel, validator
from pydantic.types import UUID
from web3 import Web3


class CreateOrder(BaseModel):
    product: UUID
    from_wallet: str

    class Config:
        orm_mode = True

    @validator("from_wallet")
    def is_wallet_address(cls, from_wallet):
        if Web3.isAddress(from_wallet):
            return from_wallet
        raise ValueError("Not valid wallet address")
