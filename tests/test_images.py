import os
from pathlib import Path

from httpx import AsyncClient

from tests.data_for_tests import good_response_image_load

_TEST_ROOT_DIR = Path(__file__).resolve().parents[1]
image_name = os.path.join(_TEST_ROOT_DIR, "tests", "image_for_test.jpg")
image = open(image_name, "rb")


async def test_add_image(ac: AsyncClient):
    """
    Тест загрузки изображения к твиту
    """
    response = await ac.post(
        "/api/medias", files={"file": image}, headers={"api-key": "test_1"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data == good_response_image_load
