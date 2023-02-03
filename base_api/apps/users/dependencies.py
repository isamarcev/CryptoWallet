# -*- coding: utf-8 -*-
from async_lru import alru_cache
from boto3 import Session
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.exeptions import UndefinedUser
from base_api.apps.users.database import UserDatabase
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.users.manager import UserManager
from base_api.apps.users.models import Permission, User
from base_api.config.db import SessionLocal, async_session
from base_api.config.settings import settings
from base_api.config.storage import Storage


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_user_db() -> UserDatabase:
    return UserDatabase(User, Permission)


async def get_jwt_backend() -> JWTBackend:
    jwt_backend = JWTBackend(
        settings.jwt_secret_key,
        settings.jwt_algorithm,
        settings.jwt_expire,
    )
    return jwt_backend


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
async def get_user_manager() -> UserManager:
    jwt_backend = await get_jwt_backend()
    user_db = await get_user_db()
    s3_client = await get_s3_client()
    storage = await get_storage(s3_client)
    return UserManager(user_db, jwt_backend, storage)


async def get_current_user(
    token: str = Depends(auth_bearer),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
    manager: UserManager = Depends(get_user_manager),
    db: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = await jwt_backend.decode_token(token)
        if payload:
            user = await manager.get_user(user_id=payload.get("id"), db=db)
        else:
            raise UndefinedUser()
    except:
        raise UndefinedUser()
    if user:
        return user
    else:
        raise UndefinedUser()
