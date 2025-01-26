from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper
from src.core.schemas.schema_images import ImageResponseSchema
from src.api.crud.crud_images import image_save

medias_route = APIRouter(prefix="/api/medias", tags=["Операции с изображениями"])


@medias_route.post(
    "",
    response_model=ImageResponseSchema,
    status_code=201,
)
async def upload_image(
    file: UploadFile,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    # Записываем изображение в файловой системе и создаем запись в БД
    image_id = await image_save(image_file=file, session=session)
    return {"media_id": image_id}
