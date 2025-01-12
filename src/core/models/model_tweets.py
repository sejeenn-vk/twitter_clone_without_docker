from typing import List
import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.sql import func

from .model_base import Base
from .model_images import Image
from .model_likes import Like


class Tweet(Base):
    """
    Модель для хранения твитов
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(280))
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    images: Mapped[List["Image"]] = relationship(
        backref="tweet", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        backref="tweet", cascade="all, delete-orphan"
    )

    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    __mapper_args__ = {"confirm_deleted_rows": False}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.content}, user_id={self.user_id})"
