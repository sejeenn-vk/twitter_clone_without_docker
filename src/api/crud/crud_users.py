from typing import Annotated, Optional, Union

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from src.core.models.db_helper import db_helper
from src.core.models.model_users import User, followers_tbl


class APITokenHeader(APIKeyHeader):
    """
    Проверка и извлечение токена (api_key) из header
    """

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        return api_key


TOKEN = Security(APITokenHeader(name="api-key"))


async def get_user(
    session: AsyncSession,
    api_key_or_id: Union[str, int],
) -> User:
    """
    Получение пользователя по его api_key или id
    :param session: асинхронная сессия
    :param api_key_or_id: личный ключ пользователя, передается в http-header
    :return: экземпляр класса User
    """
    if isinstance(
        api_key_or_id, str
    ):  # проверяем какого типа входящая переменная
        parameter = User.api_key
    else:
        parameter = User.id
    stmt = (
        select(User)
        .where(parameter == api_key_or_id)
        .options(
            joinedload(User.followers).load_only(User.id, User.name),
            joinedload(User.followed).load_only(User.id, User.name),
        )
    )
    response = await session.scalars(stmt)
    user = response.unique().one()
    return user


async def get_current_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    token: str = TOKEN,
):
    """
    Получение текущего пользователя из http-header по
    его api_key
    :param session: асинхронная сессия
    :param token: токен api_key
    :return: экземпляр класса User
    """
    stmt = (
        select(User)
        .where(User.api_key == token)
        .options(joinedload(User.followed).load_only(User.id, User.name))
    )
    response = await session.scalars(stmt)
    user = response.unique().one()
    return user


async def unsubscribe_from_user(
    user: User, user_id: int, session: AsyncSession
):
    stmt = delete(followers_tbl).where(
        followers_tbl.c.follower_id == user.id,
        followers_tbl.c.followed_id == user_id,
    )
    await session.execute(stmt)
    await session.commit()


async def subscribe_to_user(user: User, user_id: int, session: AsyncSession):
    stmt = insert(followers_tbl).values(
        follower_id=user.id, followed_id=user_id
    )
    await session.execute(stmt)
    await session.commit()
