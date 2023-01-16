from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .dependencies import get_db, get_user_manager
from .manager import UserManager
from .models import User
from fastapi import APIRouter, Depends, Response
from . import database
from .schemas import UserRegister, UserLogin
from ...config.db import get_session


user_router = APIRouter(
    prefix='/users',
    tags=['apps']
)


@user_router.post('/register/',
                  status_code=status.HTTP_201_CREATED)
async def register(
        user: UserRegister,
        response: Response,
        session: AsyncSession = Depends(get_session),
        user_manager: UserManager = Depends(get_user_manager),

):
    print(user)
    result = await user_manager.create_user(user=user, session=session)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {result.get('access_token')}",
    )

    return result


@user_router.post("/login/",
                  status_code=status.HTTP_200_OK)
async def login(
        user: UserLogin,
        response: Response,
        session: AsyncSession = Depends(get_session),
        user_manager: UserManager = Depends(get_user_manager),
):
    result = await user_manager.login(user, session)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {result.get('access_token')}",
    )
    return result
