from http import HTTPStatus

from api.v1.queries.genre_person import query_genre_person
from api.v1.schemas.genre_person import GenrePersonDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from services.collection import CollectionService
from services.detail import DetailService
from utils.service import get_collection_service, get_detail_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=Page[GenrePersonDetailSchema])
async def actor_collection(
    actors_service: CollectionService = Depends(get_collection_service),
) -> list[GenrePersonDetailSchema]:
    """Get actors collection with related films ordered by rating."""
    actors = await actors_service.get_items(
        query_genre_person(), GenrePersonDetailSchema, CONFIG["ELASTIC_ACTORS_INDEX"]
    )
    if not actors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="actors not found")
    return paginate(actors)


@router.get("/{actor_id}", response_model=GenrePersonDetailSchema)
async def actor_detail(
    actor_id: str, actor_service: DetailService = Depends(get_detail_service)
) -> GenrePersonDetailSchema:
    """Get one actor with related films ordered by rating."""
    actor = await actor_service.get_item_by_id(GenrePersonDetailSchema, CONFIG["ELASTIC_ACTORS_INDEX"], actor_id)
    if not actor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="actor not found")
    return actor
