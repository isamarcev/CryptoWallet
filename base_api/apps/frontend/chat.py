from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Response


templates = Jinja2Templates(directory="templates")


chat_router = APIRouter()


@chat_router.get("/chat", include_in_schema=False)
async def register(
        request: Request,
):
    print(request, "REQUEST")
    return templates.TemplateResponse("chat/chat.html", context={"request": request})

