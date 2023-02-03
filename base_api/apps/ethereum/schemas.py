from pydantic import BaseModel
from pydantic.types import UUID


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