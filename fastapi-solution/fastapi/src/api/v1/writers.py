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
async def writer_collection(
    writers_service: CollectionService = Depends(get_collection_service),
) -> list[GenrePersonDetailSchema]:
    """Get writers collection with related films ordered by rating."""
    writers = await writers_service.get_items(
        query_genre_person(), GenrePersonDetailSchema, CONFIG["ELASTIC_WRITERS_INDEX"]
    )
    if not writers:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="writers not found")
    return paginate(writers)


@router.get("/{writer_id}", response_model=GenrePersonDetailSchema)
async def actor_detail(
    writer_id: str, writer_service: DetailService = Depends(get_detail_service)
) -> GenrePersonDetailSchema:
    """Get one writer with related films ordered by rating."""
    writer = await writer_service.get_item_by_id(GenrePersonDetailSchema, CONFIG["ELASTIC_WRITERS_INDEX"], writer_id)
    if not writer:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="writer not found")
    return writer
