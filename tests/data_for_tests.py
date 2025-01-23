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
