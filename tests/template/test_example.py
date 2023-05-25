from http import HTTPStatus

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.example.models import TestTable
from tests.requests.example import example_get_request


@pytest.mark.asyncio
async def test_index(client: TestClient, session: AsyncSession):
    session = session
    example_id = 1
    session.add(TestTable(test_field=example_id))
    await session.commit()

    response = await example_get_request(client, example_id)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_index_not_found(client: TestClient):
    example_id = 69

    response = await example_get_request(client, example_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
