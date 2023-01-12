import uuid

from fastapi import FastAPI

from sqlalchemy.dialects.postgresql import UUID

from base_api.config.db import engine, metadata, database
from pydantic import BaseModel
from base_api.apps.users.models import perm


metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserCreate(BaseModel):
    has_chat_access: bool


async def create_user(user: UserCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    print('444444')
    db_user = perm.insert().values(**user.dict())
    user_id = await database.execute(db_user)
    return UserCreate(**user.dict())


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.post("/users/", response_model=UserCreate)
async def create(user: UserCreate):
    print('---------*********---------')
    return await create_user(user=user)
