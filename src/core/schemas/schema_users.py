from pydantic import BaseModel, ConfigDict, Field


class BaseUserSchema(BaseModel):
    id: int = 10050
    name: str = "Василий Пупкин"


class UserSchema(BaseModel):
    id: int = 1
    name: str = "Лев Толстой"
    followers: list[BaseUserSchema]
    following: list[BaseUserSchema]


class FullUserSchema(BaseModel):
    result_user: bool = Field(alias="result", default=True)
    user: UserSchema


class CreateUserSchema(BaseModel):
    name: str = Field(default="Имя Фамилия")
    api_key: str = Field(default="api_key должен быть уникальным")


class UserReadSchema(CreateUserSchema):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
