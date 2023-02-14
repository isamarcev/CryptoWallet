# -*- coding: utf-8 -*-
from async_lru import alru_cache
from boto3 import Session
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from sqlalchemy.ext.asyncio import AsyncSession

import aioredis
from aioredis import Redis


from base_api.apps.chat.dependencies import get_s3_client, get_storage
from base_api.apps.chat.exeptions import UndefinedUser
from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.models import Wallet, Transaction
from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.users.database import UserDatabase
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.ibay.manager import IbayManager
from base_api.apps.ibay.models import Product, Order
from base_api.base_api_producer import BaseApiProducer
from base_api.config.db import SessionLocal, async_session
from base_api.config.settings import settings
from base_api.apps.ethereum.web3_client import EthereumClient

from base_api.config.storage import Storage


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_ibay_db() -> IbayDatabase:
    return IbayDatabase(Product, Order)


async def get_eth_db() -> EthereumDatabase:
    return EthereumDatabase(Wallet, Transaction)


@alru_cache
async def get_producer() -> BaseApiProducer:
    return BaseApiProducer()


async def get_redis() -> Redis:
    redis = aioredis.from_url(settings.redis_url)
    return redis


async def get_client() -> EthereumClient:
    return EthereumClient()


@alru_cache()
async def get_ibay_manager() -> IbayManager:
    user_db = await get_ibay_db()
    s3_client = await get_s3_client()
    eth_client = await get_client()
    storage = await get_storage(s3_client)
    ethereum_db = await get_eth_db()
    producer = await get_producer()
    redis = await get_redis()
    return IbayManager(user_db, storage, ethereum_db, producer, eth_client, redis)
