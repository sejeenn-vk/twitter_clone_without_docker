import os
import aiofiles
from loguru import logger
from typing import List
from http import HTTPStatus
from contextlib import suppress
from datetime import datetime
from fastapi import UploadFile


from src.core.config import ALLOWED_EXTENSIONS, IMAGES_FOLDER
from src.core.models.model_images import Image
from src.utils.exeptions import CustomApiException


def allowed_image(image_name: str) -> None:
    """
    Проверка расширения изображения
    :param image_name: название изображения
    :return: None
    """

    # Проверяем, что расширение текущего файла есть в списке разрешенных
    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    if "." in image_name and image_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
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


async def writing_file_to_hdd(file: UploadFile, avatar=False) -> str:
    """
    Сохранение изображения
    :param avatar: переключатель для сохранения аватара пользователя или изображения к твиту
    :param image: файл - изображение
    :return: путь относительно static для сохранения в БД
    """
    # Проверка формата загружаемого файла
    allowed_image(image_name=file.filename)

    with suppress(OSError):
        if avatar:
            logger.debug("Сохранение аватара пользователя")
            path = os.path.join(IMAGES_FOLDER, "avatars")

        else:
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

        contents = file.file.read()
        full_path = os.path.join(path, f"{file.filename}")

        # Сохраняем изображение
        async with aiofiles.open(full_path, mode="wb") as f:
            await f.write(contents)

        # Возвращаем очищенную строку для записи в БД
        return clear_path(path=full_path)


async def delete_image_from_hdd(images: List[Image]):
    """
    Удаление картинки с жесткого диска
    :param images: список объектов Image
    :return: None
    """
    logger.debug(f"Удаление изображений из файловой системы")
    # folder = os.path.join(
    #     "static", images[0].path_media.rsplit("/", 1)[0].rsplit("\\", 1)[0]
    # )
    print(os.path.join("static", images[0].path_media))
    # os.remove(os.path.join("static", images[0].path_media))
    # logger.debug(f"Изображение №{images[0].id} - {images[0].path_media} удалено")


async def delete_image(images: List[Image]) -> None:
    # Директория с изображениями к твиту
    folder = os.path.join(
        "static", images[0].path_media.rsplit("/", 1)[0].rsplit("\\", 1)[0]
    )

    for img in images:
        try:
            # Удаляем каждое изображение из файловой системы
            os.remove(os.path.join("static", img.path_media))
            logger.debug(f"Изображение №{img.id} - {img.path_media} удалено")

        except FileNotFoundError:
            logger.error(f"Директория: {img.path_media} не найдена")

    logger.info("Все изображения удалены")

    # Проверка и очистка директории, если пустая
    await check_and_delete_folder(path=folder)


async def check_and_delete_folder(path: str) -> None:
    """
    Проверка и удаление папки, если пуста (подчистка пустых директорий после удаления твитов с изображениями)
    :param path: директория с изображениями после удаления твита
    :return: None
    """
    try:
        # Удаляем папку, если пустая
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            logger.info(f"Директория: {path} удалена")

    except FileNotFoundError:
        logger.error(f"Директория: {path} не найдена")
