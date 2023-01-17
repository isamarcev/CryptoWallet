from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Response


templates = Jinja2Templates(directory="templates")


auth_router = APIRouter()


@auth_router.get("/register", include_in_schema=False)
async def register(
        request: Request,
):
    print(request, "REQUEST")
    return templates.TemplateResponse("users/registration.html", context={"request": request})

