from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.db_helper import db_helper
from src.core.schemas.schema_users import (
    FullUserSchema,
    UserReadSchema,
    CreateUserSchema,
)
from src.api.crud import crud_users

users_route = APIRouter(prefix="/api/users")


@users_route.get(
    "/me",
    tags=["Получение данных текущего пользователя"],
    response_model=FullUserSchema,
)
async def get_users_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    api_key: Annotated[str | None, Header()] = None,
):
    user = await crud_users.get_user_by_api_key(session=session, api_key=api_key)
    data = {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [{"id": u.id, "name": u.name} for u in user.followers],
            "following": [{"id": u.id, "name": u.name} for u in user.followed],
        },
    }
    return data


@users_route.post(
    "/me", tags=["Создать нового пользователя"], response_model=UserReadSchema
)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_create: CreateUserSchema,
):
    user = await crud_users.create_user(session=session, user_create=user_create)
    return user


@users_route.get(
    "/{user_id}",
    response_model=FullUserSchema,
    tags=["Получение данных пользователя по его user_id"],
)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    user = await crud_users.get_user_by_user_id(session=session, user_id=user_id)
    data = {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [{"id": u.id, "name": u.name} for u in user.followers],
            "following": [{"id": u.id, "name": u.name} for u in user.followed],
        },
    }
    return data
