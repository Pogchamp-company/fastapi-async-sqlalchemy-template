import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from app.core.config import settings
# from starlette.testclient import TestClient

from manage import app


# @pytest.fixture
# def client():
#     with TestClient(app) as client:
#         yield client

@pytest_asyncio.fixture
async def client():
    scope = {"client": (settings.HOST, str(settings.PORT))}

    async with TestClient(
        app, scope=scope
    ) as client:
        yield client
