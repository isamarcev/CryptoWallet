# -*- coding: utf-8 -*-
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.schemas import UserLogin, UserProfileUpdate, UserRegister

from .exeptions import UsernameAlreadyExists
from .jwt_backend import JWTBackend
from .models import User
from .utils.password_hasher import get_password_hash, verify_password
from .utils.validators import validate_email_, validate_register, validate_update_profile, validate_username


class UserManager:
    def __init__(
        self,
        database: UserDatabase,
        jwt_backend: JWTBackend,
    ):
        self.database = database
        self.jwt_backend = jwt_backend

    @staticmethod
    async def get_payload(user_data: User):
        payload = {
            "id": str(user_data.id),
            "username": user_data.username,
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

    async def login(self, user: UserLogin, session: AsyncSession) -> Dict:
        # validated_email = await validate_email_(user.email)
        # if not validated_email.get("valid"):
        #     raise HTTPException(status_code=400, detail=validated_email.get("invalid"))
        # user.email = validated_email.get("valid")
        user_instance = await self.database.get_user_by_email(user.email, session)
        if user_instance and verify_password(user.password, user_instance.password):
            payload = await self.get_payload(user_instance)
            result = await self.jwt_backend.create_access_token(payload)
            result[0]["access_token"] = result[-1]
            return result[0]
        else:
            raise HTTPException(status_code=404, detail="User with this email does not exist or password with mistakes")

    async def get_user(self, user_id: str, db: AsyncSession) -> User:
        return await self.database.get_user_by_id(user_id, db)

    async def collect_profile_info(self, user) -> Dict:
        profile_info = {
            "email": user.email,
            "username": user.username,
        }
        return profile_info

    async def update_user_profile(
        self,
        user_data: UserProfileUpdate,
        current_user: User,
        session: AsyncSession,
    ) -> User:
        if user_data.password:
            user_data.password = get_password_hash(user_data.password)
        else:
            user_data.password = current_user.password
        if user_data.username != current_user.username:
            is_user_exists = await self.database.get_user_by_username(user_data.username, session)
            if is_user_exists:
                raise UsernameAlreadyExists()
        avatar = user_data.avatar
        if avatar:
            print(avatar.filename)
            print(avatar.content_type)
        new_data = {
            "username": user_data.username,
            "password": user_data.password,
            "photo": user_data.avatar,
        }
        result = await self.database.update_user(current_user.id, new_data, session)
        return result
