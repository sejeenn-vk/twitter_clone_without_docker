import os
from contextlib import suppress
from datetime import datetime
from http import HTTPStatus

import aiofiles
from fastapi import UploadFile
from loguru import logger

from src.core.config import ALLOWED_EXTENSIONS, IMAGES_FOLDER, STATIC_FOLDER
from src.utils.exeptions import CustomApiException


def allowed_image(image_name: str) -> None:
    """
    Проверка расширения изображения
    :param image_name: название изображения
    :return: None
    """

    # Проверяем, что расширение текущего файла есть в списке разрешенных
    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    if (
        "." in image_name
        and image_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    ):
        logger.info("Формат изображения корректный")
    else:
        logger.error("Неразрешенный формат изображения")

        raise CustomApiException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
            detail=f"The image has an unresolved format. You can only download the following formats: "
            f"{', '.join(ALLOWED_EXTENSIONS)}",
        )


def clear_path(path: str) -> str:
    """
    Очистка входной строки от "static"
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split("static")[1][1:]


async def create_directory(path: str) -> None:
    """
    Создаем папку для сохранения изображений
    """
    logger.debug(f"Создание директории: {path}")
    os.makedirs(path)  # Создание нескольких вложенных папок


async def writing_file_to_hdd(image_file: UploadFile) -> str:
    """
    Сохранение изображения
    :param image_file: файл - изображение
    :return: путь относительно static для сохранения в БД
    """
    # Проверка формата загружаемого файла
    allowed_image(image_name=image_file.filename)

    with suppress(OSError):
        logger.debug("Сохранение изображения к твиту")
        # Сохраняем изображения в директорию по дате добавления твита
        current_date = datetime.now()
        path = os.path.join(
            IMAGES_FOLDER,
            "tweets",
            f"{current_date.year}",
            f"{current_date.month}",
            f"{current_date.day}",
        )

        # Создаем директорию для картинки, если ее нет
        if not os.path.isdir(path):
            await create_directory(path=path)

        contents = image_file.file.read()
        full_path = os.path.join(path, f"{image_file.filename}")

        # Сохраняем изображение
        async with aiofiles.open(full_path, mode="wb") as f:
            await f.write(contents)

        # Возвращаем очищенную строку для записи в БД
        return clear_path(path=full_path)


async def delete_image_from_hdd(images):
    """
    Удаление картинки с жесткого диска
    :param images: список объектов Image
    :return: None
    """
    logger.debug(f"Удаление изображений из файловой системы")
    try:
        os.remove(os.path.join(STATIC_FOLDER, images[0].path_media))
        logger.debug(f"Изображение - {images[0].path_media} удалено")
    except FileNotFoundError:
        logger.debug(f"Файл {images[0].path_media} не найден")
