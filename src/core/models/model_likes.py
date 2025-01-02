from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .model_base import Base


class Like(Base):
    """
    Модель для хранения данных о лайках к твитам
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))

    def __repr__(self):
        return (f"Like(id={self.id}, user_id={self.user_id}, "
                f"tweet_id={self.tweet_id})")
    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    __mapper_args__ = {"confirm_deleted_rows": False}
