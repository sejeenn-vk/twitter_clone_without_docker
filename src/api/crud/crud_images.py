from fastapi import UploadFile
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.model_images import Image
from src.utils.image_files import writing_file_to_hdd


async def image_save(image_file: UploadFile, session: AsyncSession) -> int:
    """
    Сохранение изображения (без привязки к твиту) на жестком диске
    """
    path = await writing_file_to_hdd(image_file=image_file)
    image_obj = Image(path_media=path)  # Создание экземпляра изображения
    session.add(image_obj)  # Добавление изображения в БД
    await session.commit()  # Сохранение в БД

    return image_obj.id


async def update_image(tweet_media_ids, tweet_id, session: AsyncSession):
    query = (
        update(Image)
        .where(Image.id.in_(tweet_media_ids))
        .values(tweet_id=tweet_id)
    )
    await session.execute(query)
    await session.commit()
