import asyncio
from typing import Any, AsyncGenerator, Annotated, Generator

import pytest
import pytest_asyncio
from fastapi import Depends
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from src.core.models import User, db_helper
from src.main import main_app

users_data = [
    {"name": "Евгений Воронцов", "api_key": "test"},
    {"name": "Владимир Ульянов", "api_key": "lenin"},
]
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
client = TestClient(main_app)


@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as async_test_client:
        yield async_test_client


@pytest.fixture(scope="session")
async def users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    """
    Пользователи для тестирования
    """
    print(
        "====5678===================+++++================843==========================="
    )
    user_1 = User(name="test-user1", api_key="test-user1")
    user_2 = User(name="test-user2", api_key="test-user2")
    user_3 = User(name="test-user3", api_key="test-user3")

    # Подписки пользователей
    user_1.following.append(user_2)
    user_2.following.append(user_1)

    session.add_all([user_1, user_2, user_3])
    await session.commit()

    return user_1, user_2, user_3
