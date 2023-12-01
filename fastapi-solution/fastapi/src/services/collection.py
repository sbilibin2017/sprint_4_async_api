import pydantic
from api.v1.schemas.film import FilmDetailSchema
from api.v1.schemas.genre_person import GenrePersonDetailSchema
from core.config import Settings
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

CONFIG = Settings().dict()


class CollectionService:
    """Class for one film representation."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_items(
        self, body: dict, model: pydantic.BaseModel, index: str
    ) -> list[GenrePersonDetailSchema] | list[FilmDetailSchema] | None:
        """Gets all films."""
        resp = await self.elastic.search(index=index, body=body, scroll=CONFIG["ELASTIC_SCROLL"])
        items = await self._collect_items(model, resp)
        return items

    async def _collect_items(
        self, model: pydantic.BaseModel, resp: AsyncElasticsearch.search
    ) -> list[GenrePersonDetailSchema] | list[FilmDetailSchema]:
        """Iterates elastic index and collects documents."""
        arr = []
        old_scroll_id = resp["_scroll_id"]
        for doc in resp["hits"]["hits"]:
            arr.append(model(**doc["_source"]))
        while len(resp["hits"]["hits"]):
            resp = await self.elastic.scroll(scroll_id=old_scroll_id, scroll=CONFIG["ELASTIC_SCROLL"])
            old_scroll_id = resp["_scroll_id"]
            for doc in resp["hits"]["hits"]:
                arr.append(model(**doc["_source"]))
        return arr
