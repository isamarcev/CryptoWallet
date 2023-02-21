import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from base_api.apps.users.schemas import UserLogin


@pytest.mark.anyio
async def test_login_200(client: AsyncClient, fastapi_app: FastAPI, get_user_data: UserLogin):
    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json=get_user_data.dict()
    )

    assert response.status_code == 200
    url_logout = fastapi_app.url_path_for("logout")
    await client.get(url_logout)

@pytest.mark.anyio
async def test_login_401(client: AsyncClient, fastapi_app: FastAPI, get_user_data: UserLogin):
    url = fastapi_app.url_path_for("login")
    get_user_data.password = "password does not exists"
    response = await client.post(
        url,
        json=get_user_data.dict()
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_too_many_requests_429(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json={}
    )
    assert response.status_code == 429


@pytest.mark.anyio
async def test_login_422(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("login")
    await asyncio.sleep(10)
    response = await client.post(
        url,
        json={}
    )
    assert response.status_code == 422