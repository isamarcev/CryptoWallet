from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.database import ChatDatabase
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.models import User


class ChatManager:

    def __init__(self, database: ChatDatabase):
        self.database = database

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        return await self.database.create_message(message, db, user)
