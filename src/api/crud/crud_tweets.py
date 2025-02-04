import datetime
from http import HTTPStatus
from typing import Sequence

from sqlalchemy import delete, desc, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.exceptions import HTTPException

from src.api.crud.crud_images import update_image
from src.core.models.model_likes import Like
from src.core.models.model_tweets import Tweet
from src.core.models.model_users import User
from src.core.schemas.schema_tweets import TweetInSchema
from src.utils.image_files import delete_image_from_hdd


async def get_all_tweets(
    session: AsyncSession,
    current_user: User,
) -> Sequence[list[Tweet]]:
    """
    Пользователь может получить ленту из твитов отсортированных в
    порядке убывания по популярности от пользователей, которых он
    читает. А так же свои собственные твиты.
    :param current_user: Текущий пользователь.
    :param session: Асинхронная сессия с БД.
    :return: Список твитов
    """
    # создадим список тех кого читаем
    followed_ids = [user.id for user in current_user.followed]
    followed_ids.append(current_user.id)

    stmt = (
        select(Tweet, func.count(Tweet.likes).label("likes_count"))
        .filter(Tweet.user_id.in_(followed_ids))
        .options(
            joinedload(Tweet.user),
            joinedload(Tweet.likes).subqueryload(Like.user),
            joinedload(Tweet.images),
        )
        .outerjoin(Tweet.likes)
        .group_by(Tweet)
        .order_by(desc("likes_count"))
    )
    response = await session.execute(stmt)
    tweets = response.unique().scalars().all()

    return tweets


async def create_tweet(
    tweet: TweetInSchema,
    session: AsyncSession,
    current_user: User,
):
    """
    Создание нового твита. С картинкой или без.
    """
    new_tweet = Tweet(
        tweet_text=tweet.tweet_data,
        user_id=current_user.id,
        created_at=datetime.datetime.now(),
    )
    # Добавляем в индекс, фиксируем, но не записываем в БД!
    session.add(new_tweet)
    await session.flush()

    # # Сохраняем изображения, если есть
    tweet_media_ids = tweet.tweet_media_ids
    if tweet_media_ids:
        # Привязываем изображения к твиту
        await update_image(
            tweet_media_ids=tweet_media_ids,
            tweet_id=new_tweet.id,
            session=session,
        )
    # Сохраняем в БД все изменения (новый твит + привязку картинок к твиту)
    await session.commit()

    return new_tweet


async def delete_tweet_from_db(
    tweet_id: int,
    session: AsyncSession,
    current_user: User,
):
    """
    Удаление твита из базы данных, и если имеются
    изображения - удаление их с жесткого диска.
    """
    tweet_stmt = (
        select(Tweet)
        .where(Tweet.id == tweet_id)
        .options(joinedload(Tweet.images))
    )
    response = await session.execute(tweet_stmt)
    tweet = response.unique().scalars().one()

    # проверяем, пользователя, свой ли твит он пытается удалить
    if tweet.user_id == current_user.id:
        # Удаляем изображения твита из файловой системы, если есть
        if tweet.images:
            await delete_image_from_hdd(tweet.images)
        # Удаляем твит из базы данных
        stmt = delete(Tweet).where(Tweet.id == tweet_id)
        await session.execute(stmt)
        await session.commit()
    else:
        raise HTTPException(
            status_code=HTTPStatus.LOCKED,  # 423
            detail="The tweet that is being accessed is locked",
        )


async def add_like_to_tweet(user, tweet_id, session):
    """
    Добавление лайка твиту tweet_id.
    """
    stmt = insert(Like).values(user_id=user.id, tweet_id=tweet_id)
    await session.execute(stmt)
    await session.commit()


async def delete_like_by_tweet(user, tweet_id, session):
    """
    Удаление лайка твиту tweet_id.
    """
    stmt = delete(Like).where(
        Like.user_id == user.id, Like.tweet_id == tweet_id
    )
    await session.execute(stmt)
    await session.commit()
