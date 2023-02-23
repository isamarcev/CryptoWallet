import asyncio
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine
from base_api.config.settings import settings

from base_api.config.celery import celery_app
from .dependencies import get_ethereum_manager


DATABASE_URL = str(settings.postgres_url)


async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    engine = create_async_engine(DATABASE_URL, future=True)
    async with engine.connect() as session:
        try:
            await func(*args, db=session)
        finally:
            await session.close()
    await engine.dispose()


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    asyncio.run(wrap_db_ctx(func, *args, **kwargs))


@celery_app.task(name="check_new_block")
def check_transactions_by_block(block_hash: str):
    ethereum_manager = asyncio.run(get_ethereum_manager())
    async_to_sync(ethereum_manager.check_transaction_in_block, block_hash)
    return
