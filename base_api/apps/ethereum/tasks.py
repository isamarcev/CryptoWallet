import asyncio
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from base_api.config.settings import settings

from base_api.config.celery import celery_app
from .dependencies import get_ethereum_manager, get_session
# from ...config.db import get_session, async_session
# from base_api.base_api_consumer import async_session
#acyncio run create async session


DATABASE_URL = str(settings.postgres_url)
engine = create_async_engine(DATABASE_URL, future=True)
Session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)



async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    engine = create_async_engine(DATABASE_URL, future=True)
    async with engine.connect() as session:
        try:
            await func(*args, db=session)
        finally:
            await session.close()
    await engine.dispose()

#
# async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
#     try:
#         await Tortoise.init(
#             config=TORTOISE_CONFIG,
#         )
#         await func(*args, **kwargs)
#     finally:
#         await Tortoise.close_connections()
#
def async_to_sync(func: Callable, *args, **kwargs) -> None:
    asyncio.run(wrap_db_ctx(func, *args, **kwargs))


# @shared_task(acks_late=True)
# def parse_base_conversions_task() -> None:
#     async_to_sync(parse_base_conversions)

@celery_app.task(name="check_new_block")
def check_transactions_by_block(block_hash: str):

    ethereum_manager = asyncio.run(get_ethereum_manager())
    async_to_sync(ethereum_manager.check_transaction_in_block, block_hash)

    # result = asyncio.run(ethereum_manager.check_transaction_in_block(block_hash, db))
    return

