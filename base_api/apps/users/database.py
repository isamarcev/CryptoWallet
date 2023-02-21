# -*- coding: utf-8 -*-
from typing import Dict, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from base_api.apps.users.models import Permission, User
from base_api.apps.users.models import user as user_table, perm as permission_table
from base_api.apps.ethereum.models import wallet as wallet_table
from base_api.apps.chat.models import message as message_table
from .schemas import UserRegister


class UserDatabase:
    """

    :param user_model: user_model
    :param permission_model: permission_model

    """

    def __init__(self, user_model: Type[User], permission_model: Type[Permission]):
        self.user_model = user_model
        self.permission_model = permission_model

    async def create_user(self, user: UserRegister, session: AsyncSession) -> User:
        user_instance = self.user_model(email=user.email, username=user.username, password=user.password)
        session.add(user_instance)
        await session.commit()
        result_1 = await session.execute(
            user_table.select().where(user_table.c.email == user_instance.email),
        )
        user_instance = self.user_model(**result_1.first()._asdict())
        permission_instance = self.permission_model(user_id=user_instance.id)
        session.add(permission_instance)
        await session.commit()
        return user_instance

    async def get_user_by_email(self, user_email: str, session: AsyncSession):
        result = await session.execute(
            user_table.select().where(user_table.c.email == user_email),
        )
        result_data = result.first()
        return None if not result_data else self.user_model(**result_data._asdict())

    async def get_user_by_username(self, username: str, session: AsyncSession):
        result = await session.execute(
            user_table.select().where(user_table.c.username == username),
        )
        result_data = result.first()
        return None if not result_data else self.user_model(**result_data._asdict())

    async def get_user_by_id(self, user_id: str, db: AsyncSession) -> User:
        result = await db.execute(
            select(self.user_model).where(user_table.c.id == user_id).options(selectinload(self.user_model.permission))
        )
        result_data = result.scalars().first()
        return result_data

    @staticmethod
    async def update_user(user_id: str, new_data: Dict, db: AsyncSession):
        query = (
            user_table.update()
            .where(user_table.c.id == user_id)
            .values(new_data)
        )
        await db.execute(query)
        await db.commit()
        return User(id=user_id, **new_data)

    @staticmethod
    async def get_user_wallets(user: User, db: AsyncSession) -> list:
        result = await db.execute(
            wallet_table.select().where(wallet_table.c.user == user.id)
        )
        results = result.all()
        return results

    @staticmethod
    async def get_count_message(user: User, db: AsyncSession) -> int:
        messages = await db.execute(
            message_table.select().where(message_table.c.user_id == user.id)
        )
        return len(messages.all()) if messages else 0

    @staticmethod
    async def set_chat_permission_db(user_id: str, db: AsyncSession):
        query = (
            permission_table.update()
            .where(permission_table.c.user_id == user_id)
            .values({'has_chat_access': True})
        )
        await db.execute(query)
        await db.commit()
