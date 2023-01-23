from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from .dependencies import get_db, get_user_manager
from .manager import UserManager
from .models import User
from fastapi import APIRouter, Depends, Response, HTTPException
from . import database
from .schemas import UserRegister, UserLogin
from ..frontend.dependecies import check_user_token
from ...config.db import get_session


user_router = APIRouter()


@user_router.post('/register/',
                  status_code=status.HTTP_201_CREATED)
async def register(
        user: UserRegister,
        response: Response,
        session: AsyncSession = Depends(get_session),
        user_manager: UserManager = Depends(get_user_manager),

):
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
        expires=result.get("expiration")
    )
    return result


@user_router.get("/profile/")
async def get_profile(
        # request: Request,
        # session: Depends(get_session),
        user_manager: UserManager = Depends(get_user_manager),
        current_user=Depends(check_user_token)
):
    if not current_user:
        raise HTTPException(status_code=403, detail="You don't have permission")
    profile_info = await user_manager.collect_profile_info(user=current_user)
    return profile_info
