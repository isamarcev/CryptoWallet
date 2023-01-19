from uuid import UUID

from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import ApiSchema, as_form
from pydantic import BaseModel
from typing import Union


@as_form
class MessageCreate(BaseModel):
    text: str
    image: Union[UploadFile, None]




