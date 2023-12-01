import pydantic
from api.v1.schemas.film import FilmDetailSchema
from api.v1.schemas.genre_person import GenrePersonDetailSchema
from core.config import Settings
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

CONFIG = Settings().dict()


class DetailService:
    """Class for one film representation."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_item_by_id(
        self, model: pydantic.BaseModel, index: str, id: str
    ) -> GenrePersonDetailSchema | FilmDetailSchema | None:
        """Gets film from_elastic by id."""
        item = await self._item_from_cache(model, id)
        if not item:
            item = await self._get_item_from_elastic(model, index, id)
            if item is not None:
                await self._put_item_to_cache(item)
        return item

    async def _get_item_from_elastic(
        self, model: pydantic.BaseModel, index: str, id: str
    ) -> GenrePersonDetailSchema | FilmDetailSchema | None:
        """Gets film if not cached."""
        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None
        return model(**doc["_source"])

    async def _item_from_cache(
        self, model: pydantic.BaseModel, id: str
    ) -> GenrePersonDetailSchema | FilmDetailSchema | None:
        """Gets film if cached."""
        data = await self.redis.get(id)
        if not data:
            return None
        return model.parse_raw(data)

    async def _put_item_to_cache(self, item: pydantic.BaseModel):
        """Update cache."""
        await self.redis.set(item.id, item.json(), CONFIG["CACHE_EXPIRE_IN_SECONDS"])
