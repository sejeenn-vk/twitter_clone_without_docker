from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.model_base import Base


class Image(Base):
    """
    Модель для хранения данных об изображениях к твитам
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True
    )
    path_media: Mapped[str]

    __mapper_args__ = {"confirm_deleted_rows": False}
