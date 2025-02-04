from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud.crud_users import (
    get_current_user,
    get_user,
    subscribe_to_user,
    unsubscribe_from_user,
)
from src.core.config import API_KEY_DEFAULT, MODEL, NAME, RESULT_STR, USER_ID
from src.core.models.db_helper import db_helper
from src.core.models.model_users import User
from src.core.schemas.schema_base import (
    ErrorResponseSchema,
    LockedResponseSchema,
    ResponseSchema,
    UnauthorizedResponseSchema,
    ValidationResponseSchema,
)
from src.core.schemas.schema_users import FullUserSchema

users_route = APIRouter(
    prefix="/api/users", tags=["Операции с пользователями"]
)


@users_route.get(
    "/me",
    response_model=FullUserSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        422: {MODEL: ValidationResponseSchema},
    },
)
async def get_users_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    api_key: Annotated[str | int, Header()] = API_KEY_DEFAULT,
):
    """
    Получение данных на текущего пользователя
    :param session: асинхронная сессия
    :param api_key: ключ, по которому идентифицируется пользователь
    :return: json с данными на пользователя
    """
    user = await get_user(session=session, api_key_or_id=api_key)
    user_data = {
        RESULT_STR: "true",
        "user": {
            USER_ID: user.id,
            NAME: user.name,
            "followers": [
                {USER_ID: follower.id, NAME: follower.name}
                for follower in user.followers
            ],
            "following": [
                {USER_ID: followed.id, NAME: followed.name}
                for followed in user.followed
            ],
        },
    }
    return user_data


@users_route.get(
    "/{user_id}",
    response_model=FullUserSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        422: {MODEL: ValidationResponseSchema},
    },
)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    """
    Получение профиля пользователя по его id
    :param api_key: ключ текущего пользователя
    :param session: асинхронная сессия
    :param user_id: id пользователя
    :return: экземпляр класса User
    """
    user = await get_user(session=session, api_key_or_id=user_id)
    user_data = {
        RESULT_STR: "true",
        "user": {
            USER_ID: user.id,
            NAME: user.name,
            "followers": [
                {USER_ID: follower.id, NAME: follower.name}
                for follower in user.followers
            ],
            "following": [
                {USER_ID: followed.id, NAME: followed.name}
                for followed in user.followed
            ],
        },
    }
    return user_data


@users_route.delete(
    "/{user_id}/follow",
    response_model=ResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        404: {MODEL: ErrorResponseSchema},
        422: {MODEL: ValidationResponseSchema},
        423: {MODEL: LockedResponseSchema},
    },
)
async def unfollow_from_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    """
    Отписаться от пользователя
    :param api_key: ключ того кто отписывается (по умолчанию - test)
    :param user_id: id-пользователя от которого хотите отписаться
    :param session: асинхронная сессия
    :param current_user: ваш текущий пользователь
    :return: json {"result": true}
    """
    await unsubscribe_from_user(
        user=current_user, user_id=user_id, session=session
    )
    return {RESULT_STR: True}


@users_route.post(
    "/{user_id}/follow",
    response_model=ResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        404: {MODEL: ErrorResponseSchema},
        422: {MODEL: ValidationResponseSchema},
        423: {MODEL: LockedResponseSchema},
    },
)
async def follow_to_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    """
    Подписаться на пользователя
    :param api_key: ключ того кто подписывается (по умолчанию - test)
    :param user_id: id-пользователя на которого подписываетесь
    :param session: асинхронная сессия
    :param current_user: ваш текущий пользователь
    :return: json {"result": true}
    """
    await subscribe_to_user(
        user=current_user, user_id=user_id, session=session
    )
    return {RESULT_STR: True}
