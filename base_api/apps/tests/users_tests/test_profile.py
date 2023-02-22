import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from base_api.apps.users.schemas import UserLogin, UserRegister

@pytest.mark.anyio
@pytest.mark.run_order(order=1)
async def test_get_profile_401(
        client: AsyncClient,
        fastapi_app: FastAPI,
):

    url = fastapi_app.url_path_for("get_profile")
    response = await client.request(
        "GET",
        url
    )
    print(response.json(), "RESPONSE JSON REGISTRATION")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_profile_200(
        client: AsyncClient,
        fastapi_app: FastAPI,
        get_token
):
    # client.headers = {
    #     "Authorization": f'Bearer {get_token.dict()["access_token"]}'
    # }
    url = fastapi_app.url_path_for("get_profile")

    response = await client.get(
        url,
    )
    print(response.json(), "RESPONSE JSON REGISTRATION")
    assert response.status_code == 200

