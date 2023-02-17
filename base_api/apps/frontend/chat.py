from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends
from base_api.apps.frontend.dependecies import check_user_token

templates = Jinja2Templates(directory="base_api/templates")


chat_router = APIRouter()


@chat_router.get("/chat", include_in_schema=False)
async def chat(
        request: Request,
        token=Depends(check_user_token),
):
    if not token:
        return RedirectResponse("/login")
    if not token.permission.has_chat_access:
        return RedirectResponse("/")
    return templates.TemplateResponse("chat/chat.html", context={"request": request})

