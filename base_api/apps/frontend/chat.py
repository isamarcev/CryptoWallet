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



@chat_router.get("/base", include_in_schema=False)
async def register(
        request: Request,
):
    print(request, "REQUEST")
    return templates.TemplateResponse("basic_template/basic.html", context={"request": request})

