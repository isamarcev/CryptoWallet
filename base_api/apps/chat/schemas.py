from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union


class MessageCreate(BaseModel):
    id: UUID
    user: UUID
    text: str
    image: Union[UploadFile, None]




