from itertools import chain
from typing import List

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from src.core.models.model_images import Image
from src.utils.images import save_image, delete_images


async def image_save(image: UploadFile, session: AsyncSession) -> int:
    """
    Сохранение изображения (без привязки к твиту)
    """
    path = await save_image(file=image)  # Сохранение изображения в файловой системе
    image_obj = Image(path_media=path)  # Создание экземпляра изображения
    session.add(image_obj)  # Добавление изображения в БД
    await session.commit()  # Сохранение в БД

    return image_obj.id
