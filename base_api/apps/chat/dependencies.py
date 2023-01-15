from async_lru import alru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.database import ChatDatabase
from base_api.apps.chat.manager import ChatManager
from base_api.apps.chat.models import Message
from base_api.config.db import SessionLocal, async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_chat_db() -> ChatDatabase:
    return ChatDatabase(Message)


@alru_cache()
async def get_chat_manager() -> ChatManager:
    chat_db = await get_chat_db()
    return ChatManager(chat_db)
