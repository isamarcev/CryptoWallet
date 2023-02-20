# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from base_api.config.settings import settings

DATABASE_URL = str(settings.postgres_url)

# ASYNC
engine = create_async_engine(DATABASE_URL, future=True)


metadata = MetaData()


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(metadata.create_all)


# я думаю что лучше просто инициировать сессию а получать ее из dependencies а не все в одно месте!!!
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
