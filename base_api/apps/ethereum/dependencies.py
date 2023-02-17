import aioredis
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.models import Wallet, Transaction
from base_api.apps.ethereum.web3_client import EthereumClient
from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.ibay.dependencies import get_ibay_manager
from base_api.apps.ibay.manager import IbayManager
from base_api.apps.ibay.models import Product, Order
from base_api.config.db import async_session
from base_api.config.settings import settings


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_db() -> EthereumDatabase:
    return EthereumDatabase(Wallet, Transaction)


async def get_client() -> EthereumClient:
    return EthereumClient()


async def get_redis() -> Redis:
    redis = aioredis.from_url(settings.redis_url)
    return redis

async def get_ethereum_manager() -> EthereumManager:
    ethereum_db = await get_db()
    eth_client = await get_client()
    redis = await get_redis()
    ibay_manager = await get_ibay_manager()
    return EthereumManager(ethereum_db, eth_client, redis, ibay_manager)
