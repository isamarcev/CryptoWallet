import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from base_api.config.celery import celery_app
from .dependencies import get_ethereum_manager, get_session
from ...config.db import get_session, async_session


@celery_app.task(name="check_new_block")
def check_transactions_by_block(block_hash: str):
    db = async_session()
    print("TASKS")
    ethereum_manager = asyncio.run(get_ethereum_manager())
    result = asyncio.run(ethereum_manager.check_transaction_in_block(block_hash, db))
    return

