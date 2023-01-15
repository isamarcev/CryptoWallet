

from pydantic import BaseModel, EmailStr
from typing import Union


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    password2: str


class UserLogin(BaseModel):
    email: str
    password: str