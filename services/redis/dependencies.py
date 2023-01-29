# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis


async def get_redis() -> Redis:
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    return redis
