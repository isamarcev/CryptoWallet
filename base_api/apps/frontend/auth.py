# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from base_api.apps.frontend.dependecies import check_user_token

templates = Jinja2Templates(directory="base_api/templates")


auth_router = APIRouter()


@auth_router.get("/register", include_in_schema=False)
async def register(
    request: Request,
    token=Depends(check_user_token),
):
    if token:
        return RedirectResponse("/")
    return templates.TemplateResponse("users/registration.html", context={"request": request})


@auth_router.get("/login", include_in_schema=False)
async def login(
    request: Request,
    token=Depends(check_user_token),
):
    if token:
        return RedirectResponse("/")
    return templates.TemplateResponse("users/login.html", context={"request": request})
