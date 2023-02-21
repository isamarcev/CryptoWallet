import pytest

from httpx import AsyncClient

# from base_api.config.app import app
#
#
# # from .config.app import app
# # from config.app import app
# # from base_api.config import app
#
#
# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
