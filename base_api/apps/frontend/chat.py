from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Response, Depends

from base_api.apps.frontend.dependecies import check_user_token

templates = Jinja2Templates(directory="templates")


chat_router = APIRouter()


@chat_router.get("/chat", include_in_schema=False)
async def register(
        request: Request,
        token=Depends(check_user_token)
):
    if not token:
        return RedirectResponse("/login")
    return templates.TemplateResponse("chat/chat.html", context={"request": request})


