import time
from typing import Union, Optional

from fastapi import Depends
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from base_api.apps.users.dependencies import get_user_manager, get_jwt_backend, get_session
from base_api.apps.users.jwt_backend import JWTBackend
from base_api.apps.users.manager import UserManager


class FrontBearerCookie(OAuth2):
    async def __call__(self, request: Request) -> Union[RedirectResponse, Optional[str]]:
        cookie_authorization = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )
        if not cookie_param and cookie_scheme.lower() != "bearer":
            return RedirectResponse("/register")
        return cookie_param


async def check_user_token(
        manager: UserManager = Depends(get_user_manager),
        jwt_backend: JWTBackend = Depends(get_jwt_backend),
        db: AsyncSession = Depends(get_session),
        token: str = Depends(FrontBearerCookie())
):
    print("CHECK TOKEN", time.time())
    try:
        payload = await jwt_backend.decode_token(token)
        print("CHECK after decode", time.time())

        if not payload:
            return None
        print("before suer after decode", time.time())

        user = await manager.get_user(user_id=payload.get("id"), db=db)
        print(" after DB", time.time())

        if not user:
            return None
        return user
    except Exception:
        return None
