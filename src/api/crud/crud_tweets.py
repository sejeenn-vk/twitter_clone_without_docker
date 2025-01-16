import datetime
from loguru import logger
from sqlalchemy import select, func, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.models import User, Tweet, Like
from src.core.schemas.schema_tweets import TweetInSchema
from src.api.crud.crud_images import update_image
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
    stmt = (
        select(Tweet, func.count(Tweet.likes).label("likes_count"))
        .filter(Tweet.user_id.in_(user.id for user in current_user.followed))
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
    list_images = result.unique().scalars().one().images

    logger.info(f"Удаление твита по его tweet_id = {tweet_id}")
    stmt = delete(Tweet).where(Tweet.id == tweet_id)

    # # Удаляем изображения твита из файловой системы
    await delete_image_from_hdd(images=list_images)
    await session.execute(stmt)
    await session.commit()
