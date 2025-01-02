from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload, defaultload

from src.core.models import User, Tweet, Like


async def get_all_tweets(
        session: AsyncSession,
        current_user: User,
):
    """
        Пользователь может получить ленту из твитов отсортированных в
        порядке убывания по популярности от пользователей, которых он
        читает.
        :param current_user:
        :param session:
        :return:
    """
    stmt = (
        select(Tweet)
        .filter(Tweet.user_id.in_(user.id for user in current_user.followed))
        .options(
            joinedload(Tweet.user),
            joinedload(Tweet.likes).subqueryload(Like.user),
            joinedload(Tweet.images),
        )
        .group_by(Tweet.id)
        .order_by(desc(func.count(Like.id)))

    )
    result = await session.execute(stmt)
    tweets = result.unique().scalars().all()
    res_all = await session.execute(stmt)
    print("=================================", res_all.unique().fetchall())
    return tweets
