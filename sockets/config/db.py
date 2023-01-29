# -*- coding: utf-8 -*-
import os

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

#
from sqlalchemy.orm import sessionmaker

from base_api.config.settings import settings

# print(settings.loc)
DATABASE_URL = str("postgresql+asyncpg://nikitin:admin@localhost/sockets_db")


# ASYNC
engine = create_async_engine(DATABASE_URL, future=True)

metadata = MetaData()


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(metadata.create_all)


# я думаю что лучше просто инициировать сессию а получать ее из dependencies а не все в одно месте!!!
# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(
#         engine, class_=AsyncSession, expire_on_commit=False
#     )
#     async with async_session() as session:
#         yield session


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# конструктор запитів бази даних
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
