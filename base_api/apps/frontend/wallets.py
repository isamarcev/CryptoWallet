from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends
from base_api.apps.frontend.dependecies import check_user_token


templates = Jinja2Templates(directory="base_api/templates")


wallets_router = APIRouter()


@wallets_router.get("/my_wallets", include_in_schema=False)
async def wallets(
        request: Request,
        token=Depends(check_user_token)
):
    if not token:
        return RedirectResponse("/login")
    return templates.TemplateResponse("wallets/wallets.html", context={"request": request})

