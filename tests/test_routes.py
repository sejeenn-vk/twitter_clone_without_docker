import pytest
from httpx import AsyncClient
from loguru import logger

#
# async def test_main_route(ac: AsyncClient) -> None:
#     response = await ac.get("http://0.0.0.0")
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_root(ac: AsyncClient):
    # Тест проверки главной страницы
    response = await ac.get("/api/users/me")
    # assert response.status_code == 200
