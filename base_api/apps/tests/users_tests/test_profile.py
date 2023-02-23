import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_profile_401(
        client: AsyncClient,
        fastapi_app: FastAPI,
):

    url = fastapi_app.url_path_for("get_profile")
    response = await client.request(
        "GET",
        url
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_profile_200(
        client: AsyncClient,
        fastapi_app: FastAPI,
        get_token
):
    url = fastapi_app.url_path_for("get_profile")
    response = await client.get(
        url,
    )
    assert response.status_code == 200

