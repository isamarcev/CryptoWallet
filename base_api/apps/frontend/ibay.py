from fastapi import APIRouter, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Response, Depends

from base_api.apps.frontend.dependecies import check_user_token


templates = Jinja2Templates(directory="base_api/templates")


front_ibay_router = APIRouter()


@front_ibay_router.get("/ibay", include_in_schema=False)
async def ibay(
        request: Request,
        token=Depends(check_user_token)
):
    if not token:
        return RedirectResponse("/login")
    return templates.TemplateResponse("ibay/ibay.html", context={"request": request})

