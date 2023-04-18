import pytest
from starlette.testclient import TestClient

from manage import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
