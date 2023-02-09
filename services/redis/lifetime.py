# # -*- coding: utf-8 -*-
# import logging
#
# from config.settings import settings
# from fastapi import FastAPI
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_limiter import FastAPILimiter
# from redis.asyncio.utils import from_url
#
# # from fastapi_limiter import FastAPILimiter
#
# logger = logging.getLogger(__name__)
#
#
# async def init_redis(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Creates connection pool for redis.
#
#     :param app: current fastapi application.
#
#     """
#     logger.info("Redis init")
#     app.state.redis = await from_url(
#         str(settings.redis_url),
#         max_connections=32,
#     )
#     # Init fastapi limiter
#     await FastAPILimiter.init(app.state.redis)
#     # Init redis backend for fastapi cache
#     app.state.redis_backend = RedisBackend(app.state.redis)
#     # Init fastapi cache
#     FastAPICache.init(app.state.redis_backend, prefix="hasher-main")
#
#
# async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Closes redis connection pool.
#
#     :param app: current FastAPI app.
#
#     """
#     logger.info("Redis shutdown")
#     await app.state.redis.connection_pool.disconnect()
