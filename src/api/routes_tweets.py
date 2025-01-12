from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud.crud_users import get_current_user
from src.api.crud import crud_tweets
from src.core.schemas.schema_tweets import TweetListSchema
from src.core.models.db_helper import db_helper
from src.core.models.model_users import User

tweets_route = APIRouter(prefix="/api/tweets")


@tweets_route.get(
    "",
    status_code=200,
    response_model=TweetListSchema,
    tags=["Получение твитов, пользователей, на которых подписан текущий пользователь"],
)
async def get_tweets_follow_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = "test",
):

    tweets = await crud_tweets.get_all_tweets(
        session=session, current_user=current_user
    )

    return {"tweets": tweets}
