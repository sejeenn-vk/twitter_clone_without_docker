from typing import Optional, Annotated

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.core.models import User, db_helper
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
