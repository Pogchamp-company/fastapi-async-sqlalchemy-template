from async_asgi_testclient import TestClient


async def example_get_request(client: TestClient, example_id: int):
    return await client.get(f'/example/{example_id}')
