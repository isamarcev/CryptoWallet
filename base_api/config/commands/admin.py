from sqlalchemy import select

from base_api.apps.users.models import User, Permission, user as user_table
from base_api.apps.users.utils.password_hasher import get_password_hash
from base_api.config.db import async_session


async def create_user_admin():
    async with async_session() as session:
        try:
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
