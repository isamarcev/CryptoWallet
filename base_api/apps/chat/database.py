from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.models import Message
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.models import User


class ChatDatabase:
    """
        :param message_model: message_model

    """
    def __init__(self, message_model: Message):
        self.message_model = message_model

    async def create_message(self, message: MessageCreate, db: AsyncSession):
        user = db.query(User).first()
        print('type = ', type(message))
        message_instance = Message(**message.dict())
        db.add(message_instance)
        await db.add(message_instance)
        await db.commit()
        return message_instance

