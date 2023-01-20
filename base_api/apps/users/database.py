import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.models import User, Permission
from typing import Type, Dict, List
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from .models import user as user_table
from databases import Database

from .schemas import UserRegister
from ...config.settings import settings
# from ...config.db import database

database = Database("postgresql+asyncpg://nikitin:admin@localhost/crypto_wallet_base")


class UserDatabase:
    """

    :param user_model: user_model
    :param permission_model: permission_model

    """
    def __init__(self, user_model: Type[User], permission_model: Type[Permission]):
        self.user_model = user_model
        self.permission_model = permission_model

    # async def get_user(self, user_id: UUID, db: Session) -> User:
    #     user = await db.query(self.user_model).filter(self.user_model.id == user_id).first()
    #     return user
    #
    # async def get_user_by_email(self, user_email: str, db: Session) -> Dict:
    #     user = await db.query(self.user_model).filter(self.user_model.email == user_email)
    #     return user

    async def create_user(self, user: UserRegister, session: AsyncSession) -> User:
        user_instance = User(email=user.email, username=user.username, password=user.password)
        session.add(user_instance)
        await session.commit()
        await session.refresh(user_instance)
        result_1 = await session.execute(
            user_table.select().where(user_table.c.username == user_instance.username)
        )
        user_instance = self.user_model(**result_1.first()._asdict())
        return user_instance

    async def get_user_by_email(self, user_email: str, session: AsyncSession):
        result = await session.execute(
            user_table.select().where(user_table.c.email == user_email)
        )
        result_data = result.first()
        print(result_data, "result data")
        return None if not result_data else self.user_model(**result_data._asdict())

    async def get_user_by_username(self, username: str, session: AsyncSession):
        result = await session.execute(
            user_table.select().where(user_table.c.username == username)
        )
        result_data = result.first()
        print(result_data, "result data username")
        return None if not result_data else self.user_model(**result_data._asdict())

    async def get_user_by_id(self, user_id: str, db: AsyncSession) -> User:
        result = await db.execute(
            user_table.select().where(user_table.c.id == user_id)
        )
        result_data = result.first()
        return None if not result_data else self.user_model(**result_data._asdict())



