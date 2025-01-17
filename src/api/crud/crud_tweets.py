import datetime
from http import HTTPStatus

from loguru import logger
from sqlalchemy import select, func, desc, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.models import User, Tweet, Like
from src.core.schemas.schema_tweets import TweetInSchema
from src.api.crud.crud_images import update_image
from src.utils.exeptions import CustomApiException
from src.utils.images import delete_image_from_hdd


async def get_tweets(
    session: AsyncSession,
    current_user: User,
):
    """
    Пользователь может получить ленту из твитов отсортированных в
    порядке убывания по популярности от пользователей, которых он
    читает.
    """
    # Чтобы можно было видеть не только твиты пользователей, но и свои
    # создается список id-пользователей на которых подписан текущий пользователь
    # плюс сам текущий пользователь
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
        .join(Tweet.likes)
        .group_by(Tweet)
        .order_by(desc("likes_count"))
    )

    # TODO: проблема данного кода в том, что если нет лайков у твита
    # TODO: твит не появится в ленте новостей

    result = await session.execute(stmt)
    tweets = result.unique().scalars().all()

    return tweets


async def create_tweet(
    tweet: TweetInSchema,
    session: AsyncSession,
    current_user: User,
):
    # tweet_data='ц' tweet_media_ids=[] как выглядит ответ от фронта
    # что нужно вставить в бд
    # {"content": "Будь здоров!", "user_id": 1, "created_at": datetime.datetime.now()}

    new_tweet = Tweet(
        content=tweet.tweet_data,
        user_id=current_user.id,
        created_at=datetime.datetime.now(),
    )
    # # Добавляем в индекс, фиксируем, но не записываем в БД!!!
    session.add(new_tweet)
    await session.flush()

    # # Сохраняем изображения, если есть
    tweet_media_ids = tweet.tweet_media_ids

    if tweet_media_ids and tweet_media_ids != []:
        # Привязываем изображения к твиту
        # для этого нужны: tweet_media_ids, new_tweet.id, session
        await update_image(
            tweet_media_ids=tweet_media_ids, tweet_id=new_tweet.id, session=session
        )
    # Сохраняем в БД все изменения (новый твит + привязку картинок к твиту)
    await session.commit()

    return new_tweet


async def delete_tweet(user: User, tweet_id: int, session: AsyncSession):

    # получаем твит, который нужно удалить, из него нужно вытащить
    # путь к файлу path_media
    tweet_stmt = (
        select(Tweet).where(Tweet.id == tweet_id).options(joinedload(Tweet.images))
    )
    result = await session.execute(tweet_stmt)
    tweet = result.unique().scalars().one()

    # проверяем, пользователя, свой ли твит он пытается удалить
    if tweet.user_id != user.id:
        logger.error("Запрос на удаление чужого твита")

        raise CustomApiException(
            status_code=HTTPStatus.LOCKED,  # 423
            detail="The tweet that is being accessed is locked",
        )
    else:
        logger.debug(f"Удаление твита по его tweet_id = {tweet_id} из базы данных")
        # Удаляем изображения твита из файловой системы, если есть
        if not tweet.images:
            logger.debug("Изображений нет, удалять нечего")
        else:
            await delete_image_from_hdd(tweet.images)
        # Удаляем твит из базы данных
        stmt = delete(Tweet).where(Tweet.id == tweet_id)
        await session.execute(stmt)
        await session.commit()
        logger.debug(f"Твит '{tweet.content[:5]}...' был удалён!")


async def add_like_to_tweet(user, tweet_id, session):
    logger.debug(
        f"Добавление лайка твиту: {tweet_id}, от пользователя user_id: {user.id}"
    )
    stmt = insert(Like).values(user_id=user.id, tweet_id=tweet_id)
    await session.execute(stmt)
    await session.commit()


async def delete_like_by_tweet(user, tweet_id, session):
    logger.debug(f"Удаление лайка твита: {tweet_id}, от пользователя: {user.id}")
    stmt = delete(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id)
    await session.execute(stmt)
    await session.commit()
