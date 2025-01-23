import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="module")
async def test_users_me(ac: AsyncClient):
    print("Test tweets")
