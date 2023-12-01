from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis
from services.collection import CollectionService
from services.detail import DetailService


@lru_cache()
def get_collection_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic)
) -> CollectionService:
    return CollectionService(redis, elastic)


@lru_cache()
def get_detail_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic)
) -> DetailService:
    return DetailService(redis, elastic)
