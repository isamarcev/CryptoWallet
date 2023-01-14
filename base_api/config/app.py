from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.models import User
from base_api.config.db import init_db, get_session
from base_api.config.routers import router
from base_api.apps.users.schemas import UserRegister

app = FastAPI()

app.include_router(router=router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/log")
async def add_song(user: UserRegister, session: AsyncSession = Depends(get_session)):
    user_instance = User(**user.dict())
    session.add(user_instance)
    await session.commit()
    await session.refresh(user_instance)
    return {'user': user.username}