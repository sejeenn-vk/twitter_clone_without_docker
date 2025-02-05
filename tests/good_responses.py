from src.core.config import NAME, RESULT_STR, TEST_USER2, USER_ID

get_tweets = {
    "tweets": [
        {
            USER_ID: 2,
            "content": "Текст для теста твита 2",
            "author": {USER_ID: 2, NAME: TEST_USER2},
            "likes": [{"user_id": 1, NAME: "Test User 1"}],
            "attachments": [],
        },
        {
            USER_ID: 1,
            "content": "Text for test tweet 1",
            "author": {USER_ID: 1, NAME: "Test User 1"},
            "likes": [{"user_id": 2, NAME: TEST_USER2}],
            "attachments": ["images/image_for_test.jpg"],
        },
    ]
}

get_user = {
    RESULT_STR: True,
    "user": {
        USER_ID: 1,
        NAME: "Test User 1",
        "followers": [{USER_ID: 2, NAME: TEST_USER2}],
        "following": [{USER_ID: 2, NAME: TEST_USER2}],
    },
}

get_result = {RESULT_STR: True}

create_tweet = {RESULT_STR: True, "tweet_id": 3}

image_load = {RESULT_STR: True, "media_id": 2}
