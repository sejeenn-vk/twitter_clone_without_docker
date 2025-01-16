from fastapi import UploadFile
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.core.models import User
from src.core.models.model_images import Image
from src.utils.images import writing_file_to_hdd


async def image_save(image_file: UploadFile, session: AsyncSession) -> int:
    """
    Сохранение изображения (без привязки к твиту)
    """
    # Сохранение изображения в файловой системе
    logger.info("Сохранение картинки на жесткий диск")
    path = await writing_file_to_hdd(file=image_file)
    image_obj = Image(path_media=path)  # Создание экземпляра изображения
    logger.info("Запись информации о картинке в БД")
    session.add(image_obj)  # Добавление изображения в БД
    await session.commit()  # Сохранение в БД

    return image_obj.id


async def update_image(tweet_media_ids, tweet_id, session: AsyncSession):
    logger.info("Обновление информации о картинке. Связь с твитом.")
    query = update(Image).where(Image.id.in_(tweet_media_ids)).values(tweet_id=tweet_id)
    await session.execute(query)
    await session.commit()
