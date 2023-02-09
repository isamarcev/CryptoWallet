import aioredis
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.models import Wallet, Transaction
from base_api.apps.ethereum.web3_client import EthereumClient
from base_api.config.db import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_db() -> EthereumDatabase:
    return EthereumDatabase(Wallet, Transaction)


async def get_client() -> EthereumClient:
    return EthereumClient()


async def get_redis() -> Redis:
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    return redis


async def get_ethereum_manager() -> EthereumManager:
    ethereum_db = await get_db()
    eth_client = await get_client()
    redis = await get_redis()
    return EthereumManager(ethereum_db, eth_client, redis)
