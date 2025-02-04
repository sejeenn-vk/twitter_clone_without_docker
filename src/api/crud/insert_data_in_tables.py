"""
Вставка некоторых данных в таблицы базы данный,
для демонстрации работы приложения.
"""

import datetime

from sqlalchemy import insert

from src.core.models.model_images import Image
from src.core.models.model_likes import Like
from src.core.models.model_tweets import Tweet
from src.core.models.model_users import User, followers_tbl

# -----------------------------------------------------------------
NAMES = (
    "Евгений Воронцов",
    "Владимир Ульянов",
    "Александр пушкин",
    "Лев Толстой",
    "Михаил Лермонтов",
)
API_KEYS = ("test", "lenin", "pushkin", "tolstoy", "lermont")
USER_DATA = zip(NAMES, API_KEYS)
USER_DATA_TPL = tuple(
    {"name": user[0], "api_key": user[1]} for user in USER_DATA
)

# -----------------------------------------------------------------
TWEET_TEXTS = (
    "Будь здоров!",
    "Всегда здоров!",
    "Ленин жил, Ленин жив, Ленин будет жить!",
    "Я помню чудное мгновенье...",
    "Белеет парус одинокой в тумане моря голубом!",
)
USER_IDS = (1, 2, 3, 4, 5)
TWEET_DATA_ZIP = zip(TWEET_TEXTS, USER_IDS)
TWEET_DATA = tuple(
    {
        "tweet_text": tweet[0],
        "user_id": tweet[1],
        "created_at": datetime.datetime.now(),
    }
    for tweet in TWEET_DATA_ZIP
)

# -----------------------------------------------------------------
LIKE_USER_IDS = (1, 2, 3, 1, 2, 1, 1, 2, 3, 4, 5)
LIKE_TWEET_IDS = (2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 5)
LIKE_DATA_ZIP = zip(LIKE_USER_IDS, LIKE_TWEET_IDS)
LIKE_DATA = tuple(
    {"user_id": like[0], "tweet_id": like[1]} for like in LIKE_DATA_ZIP
)

# -----------------------------------------------------------------
FOLLOWED_DATA = (
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 1, "followed_id": 3},
    {"follower_id": 1, "followed_id": 5},
)

# -----------------------------------------------------------------
IMAGE_DATA = ({"tweet_id": 5, "path_media": "images/111.jpg"},)


async def insert_data(conn):
    await conn.execute(insert(User), USER_DATA_TPL)
    await conn.execute(insert(Tweet), TWEET_DATA)
    await conn.execute(insert(Like), LIKE_DATA)
    await conn.execute(insert(followers_tbl), FOLLOWED_DATA)
    await conn.execute(insert(Image), IMAGE_DATA)
