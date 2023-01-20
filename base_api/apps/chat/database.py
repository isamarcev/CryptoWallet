from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.models import Message
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.models import User
from base_api.apps.users.models import user as user_table


class ChatDatabase:
    """
        :param message_model: message_model

    """
    def __init__(self, message_model: Message):
        self.message_model = message_model

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        message_instance = Message(**message.dict(), user=user.id, datetime=datetime.now())
        db.add(message_instance)
        await db.commit()
        return message_instance
