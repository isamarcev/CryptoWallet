from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles
from base_api.apps.frontend.auth import auth_router
from base_api.apps.users.models import User
from base_api.config.db import init_db, get_session
from base_api.config.routers import router
from base_api.apps.users.schemas import UserRegister


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=router)
    app.include_router(auth_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db()
