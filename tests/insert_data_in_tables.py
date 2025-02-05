import datetime

from sqlalchemy import insert

from src.core.models.model_images import Image
from src.core.models.model_likes import Like
from src.core.models.model_tweets import Tweet
from src.core.models.model_users import User, followers_tbl

USER_ID = "user_id"

users_data = [
    {"name": "Test User 1", "api_key": "test_1"},
    {"name": "Тестовый Пользователь 2", "api_key": "test_2"},
]

tweet_data = [
    {
        "tweet_text": "Text for test tweet 1",
        USER_ID: 1,
        "created_at": datetime.datetime.now(),
    },
    {
        "tweet_text": "Текст для теста твита 2",
        USER_ID: 2,
        "created_at": datetime.datetime.now(),
    },
]

like_data = [
    {USER_ID: 1, "tweet_id": 2},
    {USER_ID: 2, "tweet_id": 1},
]

followed_data = [
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 2, "followed_id": 1},
]

image_data = [
    {"tweet_id": 1, "path_media": "images/image_for_test.jpg"},
]


async def insert_data(conn):
    await conn.execute(insert(User), users_data)
    await conn.execute(insert(Tweet), tweet_data)
    await conn.execute(insert(Like), like_data)
    await conn.execute(insert(followers_tbl), followed_data)
    await conn.execute(insert(Image), image_data)
