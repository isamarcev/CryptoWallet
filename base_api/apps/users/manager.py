from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.schemas import UserRegister


class UserManager:

    def __init__(self, database: UserDatabase):
        self.database = database

    async def create_user(self, user: UserRegister, session: AsyncSession):
        return await self.database.create_user(user, session)

