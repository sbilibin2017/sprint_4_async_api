from http import HTTPStatus
from unittest.mock import patch

import pytest
from core.config import Settings
from httpx import AsyncClient
from main import app
from mock_data import get_item_by_id_mock, get_items_mock, get_search_mock

CONFIG = Settings().dict()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.mark.anyio
async def test_id(client):
    hdr = {"Content-Type": "application/json"}
    router_types_id = {
        "films": "2dd036a4-f5d0-4e81-8073-a36da2a684b7",
        "genres": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
        "actors": "c6842b76-4f75-4933-931c-8d5fc2469375",
        "writers": "038267d1-6ac4-4ca6-81dc-bab21466269b",
        "directors": "232fd5ab-166f-47e4-afe1-28d3450721d5",
    }
    for router_type in router_types_id.keys():
        url = f"/api/v1/{router_type}/{router_types_id[router_type]}"
        with patch("services.detail.DetailService.get_item_by_id", return_value=get_item_by_id_mock(router_type)) as p:
            response = await client.get(url=url, headers=hdr)
            assert response.status_code == HTTPStatus.OK


@pytest.mark.anyio
async def test_film_error_id(client):
    hdr = {"Content-Type": "application/json"}
    router_types_id = {
        "films": "2dd036a4",
        "genres": "3d8d9bf5",
        "actors": "c6842b76",
        "writers": "038267d1",
        "directors": "232fd5ab",
    }
    for router_type in router_types_id.keys():
        url = f"/api/v1/{router_type}/{router_types_id[router_type]}"
        with patch("services.detail.DetailService.get_item_by_id", return_value=None) as p:
            response = await client.get(url=url, headers=hdr)
            assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.anyio
async def test_error_collection(client):
    hdr = {"Content-Type": "application/json"}
    query = {"page": 1, "size": 10}
    router_types = ["films", "genres", "actors", "writers", "directors"]
    for router_type in router_types:
        url = f"/api/v1/{router_type}/"
        with patch("services.collection.CollectionService.get_items", return_value=None) as p:
            response = await client.get(url=url, headers=hdr, params=query)
            assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.anyio
async def test_film_collection(client):
    hdr = {"Content-Type": "application/json"}
    query = {"page": 1, "size": 3}
    router_types = ["films", "genres", "actors", "writers", "directors"]
    for router_type in router_types:
        url = f"/api/v1/{router_type}/"
        with patch("services.collection.CollectionService.get_items", return_value=get_items_mock(router_type)) as p:
            response = await client.get(url=url, headers=hdr, params=query)
            assert response.status_code == HTTPStatus.OK


@pytest.mark.anyio
async def test_search(client):
    hdr = {"Content-Type": "application/json"}
    query = {"title": "movie", "page": 1, "size": 3}
    with patch(
        "services.collection.CollectionService.get_items",
        return_value=get_search_mock(),
    ) as p:
        response = await client.get(url="/api/v1/search/", headers=hdr, params=query)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.anyio
async def test_error_search(client):
    hdr = {"Content-Type": "application/json"}
    query = {"title": "sdfkjn", "page": 1, "size": 3}
    with patch(
        "services.collection.CollectionService.get_items",
        return_value=None,
    ) as p:
        response = await client.get(url="/api/v1/search/", headers=hdr, params=query)
        assert response.status_code == HTTPStatus.NOT_FOUND
