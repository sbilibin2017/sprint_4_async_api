from http import HTTPStatus

from api.v1.queries.film import query_films, query_films_by_genre
from api.v1.schemas.film import FilmDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, paginate
from services.collection import CollectionService
from services.detail import DetailService
from utils.service import get_collection_service, get_detail_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=Page[FilmDetailSchema])
async def film_collection(
    request: Request, films_service: CollectionService = Depends(get_collection_service)
) -> list[FilmDetailSchema]:
    """Get paginated film collection with genres filter and ordered by date."""
    params = request.query_params
    if "genres" in params.keys():
        genres = params["genres"].split(",")
        query = query_films_by_genre(genres)
    else:
        query = query_films()
    films = await films_service.get_items(query, FilmDetailSchema, CONFIG["ELASTIC_MOVIES_INDEX"])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return paginate(films)


@router.get("/{film_id}", response_model=FilmDetailSchema)
async def film_detail(film_id: str, film_service: DetailService = Depends(get_detail_service)) -> FilmDetailSchema:
    """Get one film with related films ordered by rating."""
    film = await film_service.get_item_by_id(FilmDetailSchema, CONFIG["ELASTIC_MOVIES_INDEX"], film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film
