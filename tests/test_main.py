from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
    data = {"status_code": 200, "detail": "ok", "result": "working"}
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == data


# from httpx import AsyncClient
#
#
# async def test_health_check(ac: AsyncClient):
#     data = {"status_code": 200, "data": None, "detail": "working"}
#
#     async for client in ac:
#         response = await client.get("/")
#         assert response.status_code == 200
#         assert response.json() == data