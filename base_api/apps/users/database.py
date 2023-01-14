import uuid

from base_api.apps.users.models import User, Permission
from typing import Type
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from .models import user as user_table
from databases import Database
from ...config.settings import settings
from ...config.db import database

# database = Database(settings.postgres_url.path)


class UserDatabase:
    """

    :param user_model: user_model
    :param permission_model: permission_model

    """
    def __init__(self, user_model: Type[User], permission_model: Type[Permission]):
        self.user_model = user_model
        self.permission_model = permission_model

    async def get_user(self, user_id: UUID, db: Session) -> User:
        user = await db.query(self.user_model).filter(self.user_model.id == user_id).first()
        return user

    async def get_user_by_email(self, user_email: str, db: Session) -> User:
        user = await db.query(self.user_model).filter(self.user_model.email == user_email)
        return user

    @staticmethod
    async def create_user(username: str, db: Session):
        db_user_instance = User(username=username, id=uuid.uuid4())
        # print(db_user_instance.id, "DB USER_instance ID")
        user_instance = user_table.insert().values(username=db_user_instance.username, id=db_user_instance.id)
        await database.connect()
        # db.add() #I CANT DO THAT
        user_id = await database.execute(user_instance)
        print(user_id, "HERE IS NONE")
        return user_id


