from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import as_form
from pydantic import BaseModel, EmailStr, root_validator
from typing import Union


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    password2: str


class UserLogin(BaseModel):
    email: str
    password: str
    remember_me: bool = False

@as_form
class UserProfileUpdate(BaseModel):
    username: str
    avatar: Union[UploadFile, None]
    password: Union[str, None]
    password2: Union[str, None]

    # @root_validator
    # def check_passwords_match(cls, values):
    #     print(values)
    #     pw1, pw2 = values.get('password'), values.get('password2')
    #     print(pw1, pw2)
    #     return values
