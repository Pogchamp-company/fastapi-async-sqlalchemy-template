from starlette.testclient import TestClient


def example_get_request(client: TestClient, example_id: int):
    return client.get(f'/example/{example_id}')
