from pydantic import BaseModel, ConfigDict
from pydantic import Field


class ResponseSchema(BaseModel):
    """
    Базовая схема для возврата успешного ответа
    """

    result: bool = True
    model_config = ConfigDict(from_attributes=True)


class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """

    id: int = Field(alias="media_id")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )


class ImagePathSchema(BaseModel):
    """
    Схема для вывода ссылки на изображения при отображении твитов
    """

    path_media: str

    model_config = ConfigDict(from_attributes=True)
