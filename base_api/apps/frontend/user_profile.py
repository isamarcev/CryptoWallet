# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from .auth import auth_router
from .dependecies import check_user_token

templates = Jinja2Templates(directory="base_api/templates")


profile_router = APIRouter()


@profile_router.get("/", include_in_schema=False)
async def user_profile(
    request: Request,
    token=Depends(check_user_token),
):
    if not token:
        return RedirectResponse("/login")
    return templates.TemplateResponse("users/user_profile.html", context={"request": request})
