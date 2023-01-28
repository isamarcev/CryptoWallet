# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis

# from services.redis.dependencies import get_redis
from sockets.apps.chat.database import ChatUsers


async def get_redis() -> Redis:
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    return redis


async def get_user_db():
    redis = await get_redis()
    chat_db = ChatUsers(redis)
    return chat_db
