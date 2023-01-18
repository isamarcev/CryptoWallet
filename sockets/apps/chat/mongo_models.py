from typing import Optional
from uuid import UUID
from datetime import datetime
from beanie import Document


class Message(Document):
    user_id: UUID
    text: str
    image: Optional[str] = None
    date: Optional[datetime]


class ChatUser(Document):
    user_id: UUID
    username: str
    sid: str



