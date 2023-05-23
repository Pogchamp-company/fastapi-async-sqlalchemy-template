from http import HTTPStatus

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.example.models import TestTable
from tests.requests.example import example_get_request


def test_index(client: TestClient, session: Session):
    example_id = 1
    session.add(TestTable(test_field=example_id))
    session.commit()

    response = example_get_request(client, example_id)
    assert response.status_code == HTTPStatus.OK


def test_index_not_found(client: TestClient, session: Session):
    example_id = 69

    response = example_get_request(client, example_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
