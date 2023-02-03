# -*- coding: utf-8 -*-
import datetime as date
from typing import Optional, Union
from uuid import UUID

from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import ApiSchema, as_form
from pydantic import BaseModel


@as_form
class MessageCreate(BaseModel):
    text: str
    image: Union[UploadFile, None]


class MessageDetail(BaseModel):
    text: str
    image: Union[None, str]
    user_id: UUID
    datetime: date.datetime
    id: UUID

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)


class MessageDetail1(BaseModel):
    text: str
    image: Union[None, str]
    user_id: UUID
    datetime: date.datetime
    id: UUID
    user_photo: Union[None, str]

    class Config:
        orm_mode = True  # или использовать вместо BaseModel ApiSchema)
