from base_api.apps.users.utils import password_hasher
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from base_api.apps.users.models import User, Permission
from base_api.config.settings import settings
from sqlalchemy import select


@pytest.mark.anyio
async def create_user(db=AsyncSession):
    db_user = User(
        username=settings.username,
        email=settings.user_email,
        password=password_hasher.get_password_hash(settings.password)
    )
    db.add(db_user)
    await db.commit()

    user = await db.execute(select(User).where(User.email == settings.user_email))
    user = user.scalar()
    assert user.email == settings.user_email
    # assert user.username == settings.username



