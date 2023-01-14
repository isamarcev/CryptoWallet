from base_api.apps.users.database import UserDatabase
from base_api.apps.users.manager import UserManager
from base_api.apps.users.models import User, Permission
from base_api.config.db import SessionLocal
from async_lru import alru_cache


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_user_db() -> UserDatabase:
    return UserDatabase(User, Permission)

@alru_cache()
async def get_user_manager() -> UserManager:
    user_db = await get_user_db()
    return UserManager(user_db)
