from typing import List

from .model_base import Base
from .model_tweets import Tweet
from .model_likes import Like
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, Integer, ForeignKey


followers_tbl = Table(
    'followers_tbl',
    Base.metadata,
    Column(
        'follower_id', Integer, ForeignKey('users.id'), primary_key=True
    ),
    Column(
        'followed_id', Integer, ForeignKey('users.id'), primary_key=True
    ),
)


class User(Base):
    """
    Модель хранения пользователей
    """
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    api_key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    tweets: Mapped[List["Tweet"]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        backref="user",
        cascade="all, delete-orphan",
    )

    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers_tbl,
        primaryjoin=followers_tbl.c.followed_id == id,
        secondaryjoin=followers_tbl.c.follower_id == id,
        back_populates="followed",
    )
    followed: Mapped[List["User"]] = relationship(
        "User",
        secondary=followers_tbl,
        primaryjoin=followers_tbl.c.follower_id == id,
        secondaryjoin=followers_tbl.c.followed_id == id,
        back_populates="followers",
        lazy="selectin",
    )
    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    __mapper_args__ = {"confirm_deleted_rows": False}

    def __repr__(self):
        return (f"User(id={self.id}, name={self.name}, "
                f"api_key={self.api_key})")
