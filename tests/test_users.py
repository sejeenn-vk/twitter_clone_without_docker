import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="module")
async def test_users_me(ac: AsyncClient):
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == 1
    assert data['user']['id'] == 1
    assert data['user']['name'] == 'Test User'
    assert data['user']['followers'][0]['id'] == 2
    assert data['user']['following'][0]['id'] == 2
    assert data['user']['followers'][0]['name'] == 'Тестовый Пользователь'
    assert data['user']['following'][0]['name'] == 'Тестовый Пользователь'


@pytest.mark.asyncio(loop_scope="module")
async def test_user_by_id(ac: AsyncClient) -> None:
    response = await ac.get("/api/users/1")
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == 1
    assert data['user']['id'] == 1
    assert data['user']['name'] == 'Test User'


@pytest.mark.asyncio(loop_scope="module")
async def test_add_follow(ac: AsyncClient) -> None:
    response = await ac.post("/api/users/1/follow", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_delete_follow(ac: AsyncClient) -> None:
    response = await ac.delete("/api/users/1/follow", headers={"api-key": "test_2"})
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == 1



