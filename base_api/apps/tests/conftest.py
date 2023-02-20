from typing import AsyncGenerator

import pytest
import pytest_asyncio


# from base_api.config.settings import settings
# from sqlalchemy.
from base_api.config.app import app
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from asgi_lifespan import LifespanManager


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name

    """
    return "asyncio"

@pytest.fixture(scope="session")
async def db_engine():
    async_engine = create_async_engine(str("sqlite://:memory"))
    metadata = MetaData()
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all())
        yield async_engine


@pytest.fixture(autouse=True)
async def initialize_db(db_engine) -> AsyncGenerator[None, None]:
    async_session = sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    db = async_session()
    print("fasdfasdf")
    # create_user(db)
    yield db

    await db_engine.close()
    # trans = await


@pytest.fixture(scope="session")
async def fastapi_app() -> FastAPI:

    return app



@pytest.fixture(scope="session")
async def client(db: AsyncSession, fastapi_app: FastAPI) -> AsyncClient:
    """
    Fixture for creating HTTP client.
    :param db: Session of DB
    :param fastapi_app: FastAPI app.
    :return: HTTPX async client.
    """
    # app.dependency_overrides[get_db] = lambda: db

    async with LifespanManager(fastapi_app):
        async with AsyncClient(app=fastapi_app, base_url="127.0.0.1") as client:
            yield client
