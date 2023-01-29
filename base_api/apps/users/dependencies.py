# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.users.manager import UserManager
from base_api.apps.users.models import Permission, User
from base_api.config.db import SessionLocal, async_session
from base_api.config.settings import settings


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
async def get_user_manager() -> UserManager:
    jwt_backend = await get_jwt_backend()
    user_db = await get_user_db()
    return UserManager(user_db, jwt_backend)


async def get_current_user(
    token: str = Depends(auth_bearer),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
    manager: UserManager = Depends(get_user_manager),
    db: AsyncSession = Depends(get_session),
) -> User:
    payload = await jwt_backend.decode_token(token)
    print("user payload - ", payload.get("id"))
    user = await manager.get_user(user_id=payload.get("id"), db=db)
    print("dep user = ", user)
    if user:
        return user
    else:
        # нужно будет райзить ошибку
        return None
