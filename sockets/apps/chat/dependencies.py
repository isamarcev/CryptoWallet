# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis
from sockets.apps.chat.database import ChatUsers
from sockets.config.settings import settings


async def get_redis() -> Redis:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return redis


async def get_user_db():
    redis = await get_redis()
    chat_db = ChatUsers(redis)
    return chat_db
