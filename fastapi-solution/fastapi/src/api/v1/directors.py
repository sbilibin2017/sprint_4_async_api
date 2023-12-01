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
async def director_collection(
    directors_service: CollectionService = Depends(get_collection_service),
) -> list[GenrePersonDetailSchema]:
    """Get directors collection with related films ordered by rating."""
    directors = await directors_service.get_items(
        query_genre_person(), GenrePersonDetailSchema, CONFIG["ELASTIC_DIRECTORS_INDEX"]
    )
    if not directors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="directors not found")
    return paginate(directors)


@router.get("/{director_id}", response_model=GenrePersonDetailSchema)
async def director_detail(
    director_id: str, director_service: DetailService = Depends(get_detail_service)
) -> GenrePersonDetailSchema:
    """Get one director with related films ordered by rating."""
    director = await director_service.get_item_by_id(
        GenrePersonDetailSchema, CONFIG["ELASTIC_DIRECTORS_INDEX"], director_id
    )
    if not director:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="director not found")
    return director
