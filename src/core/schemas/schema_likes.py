from pydantic import BaseModel, Field, model_validator, ConfigDict


class LikeSchema(BaseModel):
    """
    Схема для вывода лайков при выводе твитов
    """

    id: int = Field(alias="user_id")
    username: str = Field(alias="name")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )

    @model_validator(mode="before")
    def extract_user(cls, data):
        """
        Метод извлекает и возвращает данные о пользователе из объекта Like
        """
        # ВАЖНО: доступ к данным пользователя возможен благодаря связыванию данных при SQL-запросе к БД
        # при выводе твитов - joinedload(Tweet.likes).subqueryload(Like.user)
        user = data.user
        return user
