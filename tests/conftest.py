from collections.abc import AsyncGenerator
from typing import Dict

import data_for_tests
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool, insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.core.config import settings
from src.core.models import db_helper
from src.core.models.model_base import Base
from src.core.models.model_images import Image
from src.core.models.model_likes import Like
from src.core.models.model_tweets import Tweet
from src.core.models.model_users import User, followers_tbl
from src.main import main_app


# Создание тестовых движка и сессии
test_engine = create_async_engine(str(settings.db.url), poolclass=NullPool, echo=False)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session


main_app.dependency_overrides[db_helper.session_getter] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(insert(User), data_for_tests.users_data)
        await conn.execute(insert(followers_tbl), data_for_tests.followed_data)
        await conn.execute(insert(Tweet), data_for_tests.tweet_data)
        await conn.execute(insert(Like), data_for_tests.like_data)
        await conn.execute(insert(Image), data_for_tests.image_data)

        await conn.commit()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as async_test_client:
        yield async_test_client
