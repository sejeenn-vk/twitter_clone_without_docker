import datetime
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.models.model_base import Base
from src.core.models.model_images import Image
from src.core.models.model_likes import Like


class Tweet(Base):
    """
    Модель для хранения твитов
    """

    tweet_length = 280
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tweet_text: Mapped[str] = mapped_column(String(tweet_length))
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

    # Отключаем проверку строк, тем самым убирая уведомление,
    # возникающее при удалении несуществующей строки
    __mapper_args__ = {"confirm_deleted_rows": False}

    def __repr__(self):
        return (
            f"Tweet(id={self.id}, tweet_text={self.tweet_text}, "
            f"created_at={self.created_at}, user_id={self.user_id},"
            f"likes={self.likes}, images={self.images})"
        )
