from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud import crud_tweets
from src.api.crud.crud_tweets import (
    add_like_to_tweet,
    delete_like_by_tweet,
    delete_tweet,
)
from src.api.crud.crud_users import get_current_user
from src.core.models.db_helper import db_helper
from src.core.models.model_users import User
from src.core.schemas.schema_tweets import (
    TweetInSchema,
    TweetListSchema,
    TweetResponseSchema,
)

tweets_route = APIRouter(prefix="/api/tweets", tags=["Операции с твитами"])


@tweets_route.get("", status_code=200, response_model=TweetListSchema)
async def get_tweets_follow_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = "test",
):
    """
    Получение твитов, отсортированных в
    порядке убывания, по популярности, от пользователей, которых он
    читает.
    """
    tweets = await crud_tweets.get_tweets(
        session=session, current_user=current_user
    )
    return {"tweets": tweets}


@tweets_route.post("", status_code=201, response_model=TweetResponseSchema)
async def create_new_tweet(
    tweet: TweetInSchema,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = "test",
):
    """
    Создание нового твита.
    """
    new_tweet = await crud_tweets.create_tweet(
        tweet=tweet, current_user=current_user, session=session
    )
    return {"tweet_id": new_tweet.id}


@tweets_route.delete("/{tweet_id}", status_code=200)
async def delete_tweet_by_tweet_id(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Удаление твита, пользователь может удалить только свой твит.
    :param tweet_id:
    :param session:
    :param current_user:
    :return: {"result": True}
    """
    await delete_tweet(user=current_user, tweet_id=tweet_id, session=session)
    return {"result": True}


@tweets_route.post("/{tweet_id}/likes")
async def add_like(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Ставим лайк твиту
    """
    await add_like_to_tweet(
        user=current_user, tweet_id=tweet_id, session=session
    )
    return {"result": True}


@tweets_route.delete("/{tweet_id}/likes")
async def delete_like(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Удаляем лайк твиту
    """
    await delete_like_by_tweet(
        user=current_user, tweet_id=tweet_id, session=session
    )
    return {"result": True}
