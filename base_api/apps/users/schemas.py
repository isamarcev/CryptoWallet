# -*- coding: utf-8 -*-
import re
from typing import Union

from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import as_form
from pydantic import BaseModel, validator


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
    reset: Union[bool, None]

    @validator("username", pre=True)
    def name_must_be_more_than_five(cls, username):
        if re.match(r"^[\w\d +]{5,40}$", username) and len([letter for letter in username if letter.isalpha()]) >= 4:
            return username
        raise ValueError("Username must contain at least: 5 to 40 characters, not special characters")

    @validator("password", pre=True)
    def validate_password(cls, password):
        if password:
            if re.match("(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}", password):
                return password
            raise ValueError(
                "Password must contain at least: one digit, "
                "one uppercase letter, one lowercase letter,"
                " one special character[$@#], 8 to 20 characters",
            )
        return None

    @validator("password2")
    def mismatch_passwords(cls, password2, values):
        print(values)
        if values.get("password") and values.get("password") != password2:
            raise ValueError("Passwords mismatch")
        return password2

