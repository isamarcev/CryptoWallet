# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_helper.schemas.examples_generate import examples_generate
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse
from .tasks import set_chat_permission_after_60s
from ...config.db import get_session
from ..frontend.dependecies import check_user_token
from .dependencies import get_current_user, get_user_manager
from .exeptions import UsernameAlreadyExists, UsernameInvalidException
from .manager import UserManager
from .models import User
from .schemas import UserLogin, UserProfileUpdate, UserRegister
from ...config.utils.fastapi_limiter import custom_callback

user_router = APIRouter()


@user_router.post("/register/", status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
async def register(
    user: UserRegister,
    response: Response,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    user_manager: UserManager = Depends(get_user_manager),
):
    result = await user_manager.create_user(user=user, session=session, background_tasks=background_tasks)
    set_chat_permission_after_60s.apply_async(args=[result[1]], countdown=60)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {result[0].get('access_token')}",
    )
    return result[0]


@user_router.post("/login/", status_code=status.HTTP_200_OK,
                  dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
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
        expires=result.get("expiration"),
    )
    return result


@user_router.get("/", status_code=status.HTTP_200_OK,
                 dependencies=[Depends(RateLimiter(times=6, seconds=10, callback=custom_callback))])
async def get_current_user(
    user: User = Depends(get_current_user),
):
    return user


@user_router.get("/profile/", dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))])
async def get_profile(
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(check_user_token),
):
    if not current_user:
        raise HTTPException(status_code=403, detail="You don't have permission")
    profile_info = await user_manager.collect_profile_info(user=current_user, db=session)
    return profile_info


@user_router.put(
    "/update/",
    responses=examples_generate.get_error_responses(
        UsernameInvalidException,
        UsernameAlreadyExists,
        auth=True,
    ),
    dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))]
)
async def update_profile(
    user: UserProfileUpdate = Depends(UserProfileUpdate.as_form),
    user_manager: UserManager = Depends(get_user_manager),
    current_user=Depends(check_user_token),
    session: AsyncSession = Depends(get_session),
):
    if not current_user:
        raise HTTPException(status_code=403, detail="You don`t have permission for this action")
    result = await user_manager.update_user_profile(user, current_user, session)
    return {
        "detail": {
            "username": result.username,
            "avatar": result.photo,
        },
    }


@user_router.get("/logout", status_code=status.HTTP_200_OK,
                 dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))])
async def logout(
    response: Response,
    user: User = Depends(get_current_user),
):
    response = RedirectResponse("/login")
    response.delete_cookie("Authorization")
    return response
