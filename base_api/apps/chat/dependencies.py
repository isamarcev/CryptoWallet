from async_lru import alru_cache
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from base_api.apps.chat.database import ChatDatabase
from base_api.apps.chat.manager import ChatManager
from base_api.apps.chat.models import Message
from base_api.base_api_producer import BaseApiProducer
from base_api.config.db import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_chat_db() -> ChatDatabase:
    return ChatDatabase(Message)


@alru_cache()
async def get_chat_manager() -> ChatManager:
    chat_db = await get_chat_db()
    producer = await get_producer()
    return ChatManager(chat_db, producer)


async def get_producer() -> BaseApiProducer:
    return BaseApiProducer()
