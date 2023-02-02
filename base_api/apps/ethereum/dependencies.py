from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.models import Wallet
from base_api.config.db import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_db() -> EthereumDatabase:
    return EthereumDatabase(Wallet)


async def get_ethereum_manager() -> EthereumManager:
    ethereum_db = await get_db()
    return EthereumManager(ethereum_db)