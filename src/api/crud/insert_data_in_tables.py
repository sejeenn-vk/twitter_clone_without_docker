import datetime

from sqlalchemy import insert
from src.core.models.model_likes import Like
from src.core.models.model_users import User, followers_tbl
from src.core.models.model_tweets import Tweet
from src.core.models.model_images import Image

users_data = [
    {"name": "Евгений Воронцов", "api_key": "test"},
    {"name": "Владимир Ульянов", "api_key": "lenin"},
    {"name": "Александр пушкин", "api_key": "pushkin"},
    {"name": "Лев Толстой", "api_key": "tolstoy"},
    {"name": "Михаил Лермонтов", "api_key": "lermont"},
]

tweet_data = [
    {"content": "Будь здоров!", "user_id": 1, "created_at": datetime.datetime.now()},
    {"content": "Всегда здоров!", "user_id": 3, "created_at": datetime.datetime.now()},
    {
        "content": "Ленин жил, Ленин жив, Ленин будет жить!",
        "user_id": 2,
        "created_at": datetime.datetime.now(),
    },
    {
        "content": "Я помню чудное мгновенье...",
        "user_id": 3,
        "created_at": datetime.datetime.now(),
    },
    {
        "content": "Белеет парус одинокой в тумане моря голубом!",
        "user_id": 5,
        "created_at": datetime.datetime.now(),
    },
]

like_data = [
    {"user_id": 1, "tweet_id": 2},
    {"user_id": 2, "tweet_id": 2},
    {"user_id": 3, "tweet_id": 2},
    {"user_id": 1, "tweet_id": 3},
    {"user_id": 2, "tweet_id": 3},
    {"user_id": 1, "tweet_id": 4},
    {"user_id": 1, "tweet_id": 5},
    {"user_id": 2, "tweet_id": 5},
    {"user_id": 3, "tweet_id": 5},
    {"user_id": 4, "tweet_id": 5},
    {"user_id": 5, "tweet_id": 5},
]

followed_data = [
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 1, "followed_id": 3},
    {"follower_id": 1, "followed_id": 5},
]

image_data = [
    {"tweet_id": 5, "path_media": "images/123.jpg"},
    {"tweet_id": 2, "path_media": "images/321.jpg"},
    {"tweet_id": 4, "path_media": "images/111.jpg"},
]


async def insert_data(conn):
    await conn.execute(insert(User), users_data)
    await conn.execute(insert(Tweet), tweet_data)
    await conn.execute(insert(Like), like_data)
    await conn.execute(insert(followers_tbl), followed_data)
    await conn.execute(insert(Image), image_data)
