# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis

# from services.redis.dependencies import get_redis
from sockets.apps.wallet.database import WalletDatabase


async def get_redis() -> Redis:
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    return redis


async def get_users_online_db():
    redis = await get_redis()
    wallet_db = WalletDatabase(redis)
    return wallet_db
