import loguru
from httpx import AsyncClient


async def test_root(ac: AsyncClient):
    """
    {'result': True, 'user': {'id': 1, 'name': 'Test User',
    'followers': [{'id': 2, 'name': 'Тестовый Пользователь'}],
    'following': [{'id': 2, 'name': 'Тестовый Пользователь'}]}}
    :param ac:
    :return:
    """
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    # assert data.result == True
    print("======================================================", data)
