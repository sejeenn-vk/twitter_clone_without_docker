from http import HTTPStatus

from pydantic import BaseModel, ConfigDict, Field


class ResponseSchema(BaseModel):
    """
    Базовая схема для возврата успешного ответа
    """

    result_user: bool = Field(alias="result", default=True)
    model_config = ConfigDict(from_attributes=True)


class ErrorResponseSchema(ResponseSchema):
    """
    Базовая схема для неуспешного ответа с типом и текстом ошибки.
    """

    result_user: bool = Field(alias="result", default=True)
    error_type: int = HTTPStatus.NOT_FOUND  # 404
    error_message: str = "Not found"


class UnauthorizedResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при ошибке авторизации.
    """

    error_type: int = HTTPStatus.UNAUTHORIZED  # 401
    error_message: str = "User authorization error"


class ValidationResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при ошибке валидации входных данных.
    """

    error_type: int = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    error_message: str = "Invalid input data"


class LockedResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при блокировке действия.
    """

    error_type: int = HTTPStatus.LOCKED  # 423
    error_message: str = "The action is blocked"


class BadResponseSchema(ResponseSchema):
    """
    Схема для ответа при отправке запроса на добавление изображения,
    но не приложив его.
    """

    error_type: int = HTTPStatus.BAD_REQUEST  # 400
    error_message: str = "The image was not attached to the request"
