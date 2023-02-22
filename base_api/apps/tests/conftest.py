from typing import AsyncGenerator

import pytest
import pytest_asyncio

from base_api.apps.tests.factories import create_user
from base_api.apps.users.dependencies import get_db
from base_api.apps.users.schemas import UserLogin, UserLoginResponse
from base_api.config.settings import settings
from base_api.config.app import app
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from asgi_lifespan import LifespanManager
from base_api.apps.users.models import User, Base


@pytest.fixture(scope="session")
async def db_engine():
    async_engine = create_async_engine(str(settings.test_db_url))
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    yield async_session


@pytest.fixture(scope="session")
async def initialize_db(db_engine) -> AsyncGenerator[None, None]:
    db = db_engine()
    try:
        await create_user(db)
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name

    """
    return "asyncio"


@pytest.fixture(scope="session")
async def fastapi_app() -> FastAPI:
    """
    Fixture for getting an object of app
    :return: FastAPI object
    """
    return app


@pytest.fixture(scope="session")
async def client(initialize_db: AsyncSession, fastapi_app: FastAPI) -> AsyncClient:
    """
    Fixture for creating HTTP` client.
    :param initialize_db: Session of DB
    :param fastapi_app: FastAPI app.
    :return: HTTPX async client.
    """
    app.dependency_overrides[get_db] = lambda: initialize_db

    async with LifespanManager(fastapi_app):
        async with AsyncClient(app=fastapi_app, base_url="http://127.0.0.1:8000", headers={}) as client:
            yield client


@pytest.fixture(scope="session")
async def get_user_data(
    fastapi_app: FastAPI,
) -> AsyncGenerator:
    """
    Fixture for get user data.
    """
    data = UserLogin(
        email=settings.user_email,
        password=settings.password,
        remember_me=True,
    )
    yield data

@pytest.fixture
async def get_token(
        fastapi_app: FastAPI,
        client: AsyncClient,
):
    data = UserLogin(
        email=settings.user_email,
        password=settings.password,
        remember_me=True,
    )
    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json=data.dict()
    )
    assert response.status_code == 200
    yield UserLoginResponse(
        **response.json()
    )
