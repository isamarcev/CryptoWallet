# -*- coding: utf-8 -*-
import time
from typing import Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from base_api.apps.users.dependencies import get_jwt_backend, get_session, get_user_manager
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.users.manager import UserManager


class FrontBearerCookie(OAuth2):
    async def __call__(self, request: Request) -> Union[RedirectResponse, Optional[str]]:
        cookie_authorization = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization,
        )
        if not cookie_param and cookie_scheme.lower() != "bearer":
            return RedirectResponse("/register")
        return cookie_param


async def check_user_token(
    manager: UserManager = Depends(get_user_manager),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
    db: AsyncSession = Depends(get_session),
    token: str = Depends(FrontBearerCookie()),
):
    try:
        payload = await jwt_backend.decode_token(token)
        if not payload:
            return None
        user = await manager.get_user(user_id=payload.get("id"), db=db)
        if not user:
            return None
        return user
    except Exception:
        return None
