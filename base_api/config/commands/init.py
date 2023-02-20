# -*- coding: utf-8 -*-
import logging

from asgi_lifespan import LifespanManager
from sqlalchemy import select

from base_api.apps.users.models import User, user as user_table, Permission
from base_api.apps.users.utils.password_hasher import get_password_hash
from base_api.config.db import async_session

logger = logging.getLogger(__name__)


class ProjectInitialization:
    @classmethod
    async def start(cls, app):
        async with LifespanManager(app):
            await cls.create_admin()

    @classmethod
    async def create_admin(cls):
        async with async_session() as session:
            try:
                result = await session.execute(
                    select(User).where(user_table.c.email == 'admin@admin.com')
                )
                user = result.scalars().first()
                if not user:
                    password = get_password_hash('Zaqwerty123@')
                    user = User(
                        email='admin@admin.com',
                        username='admin',
                        password=password
                    )
                    session.add(user)
                    await session.commit()
                    result = await session.execute(
                        select(User).where(user_table.c.email == user.email)
                    )
                    user = result.scalars().first()
                    permission_instance = Permission(user_id=user.id, has_chat_access=True, is_admin=True)
                    session.add(permission_instance)
                    await session.commit()
            finally:
                await session.close()
