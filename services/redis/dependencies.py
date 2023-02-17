# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis

from base_api.config.settings import settings


async def get_redis() -> Redis:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return redis
