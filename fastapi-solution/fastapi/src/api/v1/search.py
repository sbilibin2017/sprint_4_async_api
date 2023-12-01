from http import HTTPStatus

from api.v1.queries.search import query_film_by_title
from api.v1.schemas.search import SearchDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, paginate
from services.collection import CollectionService
from utils.service import get_collection_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=Page[SearchDetailSchema])
async def search_collection(
    title: str, request: Request, search_service: CollectionService = Depends(get_collection_service)
) -> list[SearchDetailSchema]:
    """Search films with title."""
    params = request.query_params
    search = None
    if len(params) != 0:
        title = params["title"]
        search = await search_service.get_items(
            query_film_by_title(title), SearchDetailSchema, CONFIG["ELASTIC_MOVIES_INDEX"]
        )
    if not search:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return paginate(search)
