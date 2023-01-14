from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.models import User
from base_api.config.db import init_db, get_session
from base_api.config.routers import router

app = FastAPI()

app.include_router(router=router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/log/{name}")
async def add_song(name: str, session: AsyncSession = Depends(get_session)):
    user = User(username=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {'user': user.username}