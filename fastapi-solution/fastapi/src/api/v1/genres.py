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
async def genres_collection(
    genres_service: CollectionService = Depends(get_collection_service),
) -> list[GenrePersonDetailSchema]:
    """Get genre collection with related films ordered by rating."""
    genres = await genres_service.get_items(
        query_genre_person(), GenrePersonDetailSchema, CONFIG["ELASTIC_GENRES_INDEX"]
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return paginate(genres)


@router.get("/{genre_id}", response_model=GenrePersonDetailSchema)
async def genres_detail(
    genre_id: str, genres_service: DetailService = Depends(get_detail_service)
) -> GenrePersonDetailSchema:
    """Get one genre with related films ordered by rating."""
    genre = await genres_service.get_item_by_id(GenrePersonDetailSchema, CONFIG["ELASTIC_GENRES_INDEX"], genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return genre
