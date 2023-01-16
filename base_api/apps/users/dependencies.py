from base_api.apps.users.database import UserDatabase
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.users.manager import UserManager
from base_api.apps.users.models import User, Permission
from base_api.config.db import SessionLocal
from async_lru import alru_cache

from base_api.config.settings import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_user_db() -> UserDatabase:
    return UserDatabase(User, Permission)


async def get_jwt_backend() -> JWTBackend:
    jwt_backend = JWTBackend(settings.jwt_secret_key,
                             settings.jwt_algorithm,
                             settings.jwt_expire)
    return jwt_backend

@alru_cache()
async def get_user_manager() -> UserManager:
    jwt_backend = await get_jwt_backend()
    user_db = await get_user_db()
    return UserManager(user_db, jwt_backend)
