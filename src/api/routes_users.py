from typing import Annotated

from fastapi import APIRouter, Depends, Header
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud import crud_users
from src.api.crud.crud_users import (
    get_current_user,
    subscribe_to_user,
    unsubscribe_from_user,
)
from src.core.models import User
from src.core.models.db_helper import db_helper
from src.core.schemas.schema_users import (
    CreateUserSchema,
    FullUserSchema,
    UserReadSchema,
)

users_route = APIRouter(
    prefix="/api/users", tags=["Операции с пользователями"]
)


@users_route.get("/me", response_model=FullUserSchema)
async def get_users_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    api_key: Annotated[str | None, Header()] = None,
):
    """
    Роут для получения пользователя с текущим api_key
    :param session:
    :param api_key:
    :return:
    """
    user = await crud_users.get_user_by_api_key(
        session=session, api_key=api_key
    )
    data = {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": u.id, "name": u.name} for u in user.followers
            ],
            "following": [{"id": u.id, "name": u.name} for u in user.followed],
        },
    }
    return data


@users_route.post("/me", response_model=UserReadSchema)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    new_user: CreateUserSchema,
):
    """
    Создание нового пользователя. В ТЗ данный роут не требовался.
    """
    user = await crud_users.create_user(session=session, user_create=new_user)
    return user


@users_route.get("/{user_id}", response_model=FullUserSchema)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    """
    Получение данных пользователя по его id
    """
    user = await crud_users.get_user_by_user_id(
        session=session, user_id=user_id
    )
    data = {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": u.id, "name": u.name} for u in user.followers
            ],
            "following": [{"id": u.id, "name": u.name} for u in user.followed],
        },
    }
    return data


@users_route.delete("/{user_id}/follow")
async def unfollow_from_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Отписаться от пользователя
    :param user_id: id-пользователя от которого хотите отписаться
    :param session: асинхронная сессия
    :param current_user: ваш текущий пользователь
    :return: json {"result": true}
    """
    await unsubscribe_from_user(
        user=current_user, user_id=user_id, session=session
    )
    return {"result": True}


@users_route.post("/{user_id}/follow")
async def follow_to_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Подписаться на пользователя
    :param user_id: id-пользователя на которого подписываетесь
    :param session: асинхронная сессия
    :param current_user: ваш текущий пользователь
    :return: json {"result": true}
    """
    await subscribe_to_user(
        user=current_user, user_id=user_id, session=session
    )
    return {"result": True}
