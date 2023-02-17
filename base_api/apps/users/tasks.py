import asyncio
from typing import Callable
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine
from base_api.config.celery import celery_app
from .dependencies import get_user_manager
from ...config.settings import settings

DATABASE_URL = str(settings.postgres_url)


async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    engine = create_async_engine(DATABASE_URL, future=True)
    redis = aioredis.from_url(settings.redis_url)
    # loop = asyncio.get_event_loop()
    async with engine.connect() as session:
        try:
            await func(*args, session=session, redis=redis)
        finally:
            await session.close()
    await engine.dispose()


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    asyncio.run(wrap_db_ctx(func, *args, **kwargs))


@celery_app.task(name="set_chat_permission")
def set_chat_permission_after_60s(user_id: str):
    user_manager = asyncio.run(get_user_manager())
    async_to_sync(user_manager.set_chat_permission, user_id)
    return
