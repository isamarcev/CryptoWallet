from sqlalchemy.ext.asyncio import AsyncSession

from sockets.apps.chat.database import ChatDatabase
from sockets.apps.chat.schemas import MessageCreate


class ChatManager:

    def __init__(self, database: ChatDatabase):
        self.database = database

    async def create_message(self, message: MessageCreate, db: AsyncSession):
        return await self.database.create_message(message, db)
