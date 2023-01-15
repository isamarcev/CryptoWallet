from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.schemas import UserRegister
from .jwt_backend import JWTBackend
from .models import User
from .utils.password_hasher import get_password_hash, verify_password
from .utils.validators import validate_email_, validate_register, validate_username


class UserManager:

    def __init__(self,
                 database: UserDatabase,
                 jwt_backend: JWTBackend):
        self.database = database
        self.jwt_backend = jwt_backend

    @staticmethod
    async def get_payload(user_data: User):
        payload = {
            "id": str(user_data.id),
            "username": user_data.username
        }
        return payload

    async def create_user(self, user: UserRegister, session: AsyncSession) -> Dict:
        errors = await validate_register(user, session, self.database)
        if errors.get("errors"):
            raise HTTPException(status_code=400, detail=errors.get("errors"))
        user.password = get_password_hash(user.password)
        new_user = await self.database.create_user(user, session)
        payload = await self.get_payload(new_user)
        result = await self.jwt_backend.create_access_token(payload)
        result[0]["access_token"] = result[-1]

        return result[0]

