import json

from httpx import AsyncClient

from tests.data_for_tests import (
    good_response_create_tweet,
    good_response_get_tweets,
    good_response_result,
)


async def test_tweets(ac: AsyncClient):
    """
    Тест получения списка твитов
    """
    response = await ac.get("/api/tweets", headers={"api-key": "test_1"})
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_get_tweets


async def test_add_new_tweet(ac: AsyncClient):
    """
    Тест создания нового твита
    """
    response = await ac.post(
        "/api/tweets",
        content=json.dumps(
            {"tweet_data": "Tweet for test", "tweet_media_ids": []}
        ),
        headers={"Content-Type": "application/json", "api-key": "test_1"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data == good_response_create_tweet


async def test_delete_tweet(ac: AsyncClient):
    """
    Тест удаления твита с tweet_id == 2
    """
    response = await ac.delete(
        "/api/tweets/2",
        headers={"Content-Type": "application/json", "api-key": "test_2"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_result


async def test_add_tweet_like(ac: AsyncClient):
    """
    Тест добавления лайка твиту tweet_id == 1
    """
    response = await ac.post(
        "/api/tweets/1/likes",
        headers={"Content-Type": "application/json", "api-key": "test_2"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data == good_response_result


async def test_delete_tweet_like(ac: AsyncClient):
    """
    Тест удаления лайка твита tweet_id == 1
    """
    response = await ac.delete(
        "/api/tweets/1/likes",
        headers={"Content-Type": "application/json", "api-key": "test_2"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data == good_response_result
