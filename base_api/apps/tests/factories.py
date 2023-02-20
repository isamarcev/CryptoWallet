from apps.users.utils import password_hasher
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.models import User, Permission

# def create_user(db=AsyncSession):
#     if not db.