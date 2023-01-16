import os

from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

#
from sqlalchemy.orm import sessionmaker

from base_api.config.settings import settings


#print(settings.loc)
DATABASE_URL = str("postgresql+asyncpg://nikitin:admin@localhost/crypto_wallet_base")


#ASYNC
engine = create_async_engine(DATABASE_URL, future=True)
# engine = create_async_engine(DATABASE_URL, echo=True, future=True)

metadata = MetaData()


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(metadata.create_all)


# я думаю что лучше просто инициировать сессию а получать ее из dependencies а не все в одно месте!!!
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

# SQLAlchemy
# engine = create_engine(DATABASE_URL)
# metadata = MetaData()
# metadata.create_all(engine)

# конструктор запитів бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
