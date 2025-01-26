import datetime

users_data = [
    {"name": "Test User", "api_key": "test_1"},
    {"name": "Тестовый Пользователь", "api_key": "test_2"},
]

tweet_data = [
    {
        "content": "Text for test tweet",
        "user_id": 1,
        "created_at": datetime.datetime.now(),
    },
    {
        "content": "Текст для теста твита",
        "user_id": 2,
        "created_at": datetime.datetime.now(),
    },
]

like_data = [
    {"user_id": 1, "tweet_id": 2},
    {"user_id": 2, "tweet_id": 1},
]

followed_data = [
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 2, "followed_id": 1},
]

image_data = [
    {"tweet_id": 1, "path_media": "images/123.jpg"},
    {"tweet_id": 2, "path_media": "images/321.jpg"},
]

good_response_get_tweets = {
    "tweets": [
        {
            "id": 2,
            "content": "Текст для теста твита",
            "author": {"id": 2, "name": "Тестовый " "Пользователь"},
            "likes": [{"user_id": 1, "name": "Test User"}],
            "attachments": ["images/321.jpg"],
        },
        {
            "id": 1,
            "content": "Text for test tweet",
            "author": {"id": 1, "name": "Test User"},
            "likes": [{"user_id": 2, "name": "Тестовый Пользователь"}],
            "attachments": ["images/123.jpg"],
        },
    ]
}

good_response_user = {
    "result": True,
    "user": {
        "id": 1,
        "name": "Test User",
        "followers": [{"id": 2, "name": "Тестовый Пользователь"}],
        "following": [{"id": 2, "name": "Тестовый Пользователь"}],
    },
}

good_response_result = {"result": True}

good_response_create_tweet = {"result": True, "tweet_id": 3}

good_response_image_load = {"result": True, "media_id": 3}
