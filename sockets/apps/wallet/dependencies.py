# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis

from sockets.apps.wallet.database import WalletDatabase
from sockets.config.settings import settings


async def get_redis() -> Redis:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return redis


async def get_users_online_db():
    redis = await get_redis()
    wallet_db = WalletDatabase(redis)
    return wallet_db
