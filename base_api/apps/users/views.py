from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db, get_user_manager
from .manager import UserManager
from .models import User
from fastapi import APIRouter, Depends
from . import database
from .schemas import UserRegister
from ...config.db import get_session


user_router = APIRouter(
    prefix='/users',
    tags=['apps']
)


@user_router.post('/register/')
async def register(
        user: UserRegister,
        session: AsyncSession = Depends(get_session),
        user_manager: UserManager = Depends(get_user_manager),
):
    response = await user_manager.create_user(user=user, session=session)
    return {"user": response.id}