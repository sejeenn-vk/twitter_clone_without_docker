from httpx import AsyncClient
from tests.data_for_tests import good_response_user, good_response_result


async def test_users_me(ac: AsyncClient):
    """
    Тест получения данных текущего пользователя
    """
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_user


async def test_user_by_id(ac: AsyncClient) -> None:
    """
    Тест получения данных пользователя id == 1
    """
    response = await ac.get("/api/users/1")
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_user


async def test_add_follow(ac: AsyncClient) -> None:
    """
    Тест добавления подписчика
    """
    response = await ac.post("/api/users/1/follow", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_result


async def test_delete_follow(ac: AsyncClient) -> None:
    """
    Тест удаления подписчика
    """
    response = await ac.delete("/api/users/1/follow", headers={"api-key": "test_2"})
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_result
