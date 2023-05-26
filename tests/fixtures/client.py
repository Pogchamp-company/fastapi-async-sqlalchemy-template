import pytest_asyncio
from async_asgi_testclient import TestClient

from app.core.config import settings
from manage import app


@pytest_asyncio.fixture
async def client():
    scope = {"test_client": (settings.HOST, str(settings.PORT))}

    async with TestClient(app, scope=scope) as test_client:
        yield test_client
