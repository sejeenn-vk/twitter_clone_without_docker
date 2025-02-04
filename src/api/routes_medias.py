from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud.crud_images import image_save
from src.core.config import API_KEY_DEFAULT, MODEL
from src.core.models.db_helper import db_helper
from src.core.schemas.schema_base import (
    BadResponseSchema,
    UnauthorizedResponseSchema,
    ValidationResponseSchema,
)
from src.core.schemas.schema_images import ImageResponseSchema

medias_route = APIRouter(
    prefix="/api/medias", tags=["Операции с изображениями"]
)


@medias_route.post(
    "",
    response_model=ImageResponseSchema,
    status_code=HTTPStatus.CREATED,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        400: {MODEL: BadResponseSchema},
        422: {MODEL: ValidationResponseSchema},
    },
)
async def upload_image(
    file: UploadFile,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    """
    Роут, отрабатывающий POST-запрос на сохранение
    изображения на жестком диске (в определенной директории)
    и запись информации о нём в БД.
    :param api_key: Ключ пользователя, который загружает изображение
    :param file: Загруженный файл изображения.
    :param session: Асинхронная сессия.
    :return: {"media_id": 100500}
    """
    image_id = await image_save(image_file=file, session=session)
    return {"media_id": image_id}
