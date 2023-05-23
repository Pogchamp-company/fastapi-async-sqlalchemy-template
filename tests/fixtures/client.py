import pytest
from starlette.testclient import TestClient

from manage import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
