from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.schemas import UserRegister
from .models import User
from .utils.password_hasher import get_password_hash
from .utils.validators import validate_email_, validate_register, validate_username


class UserManager:

    def __init__(self, database: UserDatabase):
        self.database = database

    @staticmethod
    async def get_payload(user_data: User):
        payload = {
            "id": user_data.id,
            "username": user_data.username
        }
        return payload

    async def create_user(self, user: UserRegister, session: AsyncSession):
        errors = await validate_register(user, session, self.database)
        if errors.get("errors"):
            raise HTTPException(status_code=400, detail=errors.get("errors"))
        user.password = get_password_hash(user.password)
        return await self.database.create_user(user, session)

