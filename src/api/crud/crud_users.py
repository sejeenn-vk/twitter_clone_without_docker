from loguru import logger
from typing import Optional, Annotated

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.core.models import User, db_helper
from src.core.models.model_users import followers_tbl
from src.core.schemas.schema_users import CreateUserSchema


class APITokenHeader(APIKeyHeader):
    """
    Проверка и извлечение токена (api_key) из header
    """

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        return api_key


TOKEN = APITokenHeader(name="api-key")


async def get_user_by_api_key(
    session: AsyncSession,
    api_key: str,
) -> User:
    stmt = (
        select(User)
        .where(User.api_key == api_key)
        .options(joinedload(User.followers).load_only(User.id, User.name))
        .options(joinedload(User.followed).load_only(User.id, User.name))
    )
    result = await session.scalars(stmt)
    return result.unique().one()


async def get_user_by_user_id(
    session: AsyncSession,
    user_id,
) -> User:
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(joinedload(User.followers).load_only(User.id, User.name))
        .options(joinedload(User.followed).load_only(User.id, User.name))
    )
    result = await session.scalars(stmt)
    return result.unique().one()


async def create_user(
    session: AsyncSession,
    user_create: CreateUserSchema,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_current_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    token: str = Security(TOKEN),
):
    stmt = (
        select(User)
        .where(User.api_key == token)
        .options(joinedload(User.followed).load_only(User.id, User.name))
    )
    result = await session.scalars(stmt)
    user = result.unique().one()
    return user


async def unsubscribe_from_user(user: User, user_id: int, session: AsyncSession):
    logger.debug(f"Пользователь {user.id} отписывается от пользователя {user_id}")
    stmt = delete(followers_tbl).where(
        followers_tbl.c.follower_id == user.id,
        followers_tbl.c.followed_id == user_id,
    )
    await session.execute(stmt)
    await session.commit()


async def subscribe_to_user(user: User, user_id: int, session: AsyncSession):
    logger.debug(f"Пользователь {user.id} подписывается на пользователя {user_id}")
    stmt = insert(followers_tbl).values(follower_id=user.id, followed_id=user_id)
    await session.execute(stmt)
    await session.commit()
