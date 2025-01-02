from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from .schema_users import BaseUserSchema
from .schema_likes import LikeSchema


class TweetResponse(BaseModel):
    """
    Схема для вывода id твита после публикации
    """
    id: int = Field(alias="tweet_id")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля

    )


class TweetOutSchema(BaseModel):
    """
    Схема для вывода твита, автора, вложенных изображений и данных по лайкам
    """

    id: int
    tweet_data: str = Field(
        alias="content", default="Белеет мой парус такой одинокий на фоне стальных кораблей."
    )
    user: BaseUserSchema = Field(alias="author")
    likes: List[LikeSchema]
    images: List[str] = Field(alias="attachments")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )


class TweetListSchema(BaseModel):
    """
    Схема для вывода списка твитов
    """

    tweets: List[TweetOutSchema]
