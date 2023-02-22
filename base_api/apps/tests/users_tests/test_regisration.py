import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from base_api.apps.users.schemas import UserLogin, UserRegister

@pytest.mark.anyio
async def test_registration_201(client: AsyncClient, fastapi_app: FastAPI):
    data = UserRegister(
        email="test_t11est@gmail.com",
        username="Test User Like",
        password="qwerty40Req!",
        password2="qwerty40Req!",
    )
    url = fastapi_app.url_path_for("register")
    response = await client.post(
        url,
        json=data.dict()
    )
    print(response.json(), "RESPONSE JSON REGISTRATION")
    assert response.status_code == 400


@pytest.mark.anyio
async def test_registration_400(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("register")
    data = UserRegister(
        email="test_test@gmail.com",
        username="Test User Like",
        password="qwerty40Req!1",
        password2="qwerty40Req!",
    )
    response = await client.post(
        url,
        json=data.dict()
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_registration_422(client: AsyncClient, fastapi_app: FastAPI):
    await asyncio.sleep(10)
    url = fastapi_app.url_path_for("register")
    response = await client.post(
        url,
        json={}
    )
    assert response.status_code == 422


