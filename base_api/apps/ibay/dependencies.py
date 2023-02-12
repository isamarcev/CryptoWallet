# -*- coding: utf-8 -*-
from async_lru import alru_cache
from boto3 import Session
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.exeptions import UndefinedUser
from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.users.database import UserDatabase
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.ibay.manager import IbayManager
from base_api.apps.ibay.models import Product, Order
from base_api.config.db import SessionLocal, async_session
from base_api.config.settings import settings
from base_api.config.storage import Storage


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_ibay_db() -> IbayDatabase:
    return IbayDatabase()


@alru_cache()
async def get_s3_client():
    session = Session()
    client = session.client('s3',
                            region_name=settings.space_region,
                            endpoint_url=str(settings.space_endpoint_url),
                            aws_access_key_id=settings.space_access_key,
                            aws_secret_access_key=settings.space_secret_key)
    return client


async def get_storage(s3_client) -> Storage:
    storage = Storage(s3_client, settings.space_name)
    return storage


@alru_cache()
async def get_ibay_manager() -> IbayManager:
    user_db = await get_ibay_db()
    s3_client = await get_s3_client()
    storage = await get_storage(s3_client)
    return IbayManager(user_db, storage)
