# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from .dependecies import check_user_token

templates = Jinja2Templates(directory="base_api/templates")


error_router = APIRouter()


@error_router.get("/page-not-found", include_in_schema=False)
async def user_profile(
    request: Request,
    token=Depends(check_user_token),
):
    if not token:
        return RedirectResponse("/login")
    return templates.TemplateResponse("errors/404.html", context={"request": request})
