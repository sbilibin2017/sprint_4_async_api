from pydantic import BaseModel
from utils.schema import (FilmDetailSchema, GenrePersonDetailSchema,
                          SearchDetailSchema)


class FilmItemData(BaseModel):
    items: list[FilmDetailSchema]


class GenrePersonItemData(BaseModel):
    items: list[GenrePersonDetailSchema]


class SearchItemData(BaseModel):
    items: list[SearchDetailSchema]


def get_item_by_id_mock(router_type: str):
    router_schema = {
        "films": FilmDetailSchema.parse_file("tests/data/get_films_by_id.json"),
        "genres": GenrePersonDetailSchema.parse_file("tests/data/get_genre_by_id.json"),
        "actors": GenrePersonDetailSchema.parse_file("tests/data/get_actors_by_id.json"),
        "writers": GenrePersonDetailSchema.parse_file("tests/data/get_writers_by_id.json"),
        "directors": GenrePersonDetailSchema.parse_file("tests/data/get_directors_by_id.json"),
    }
    return router_schema[router_type]


def get_items_mock(router_type: str):
    router_schema = {
        "films": FilmItemData.parse_file("tests/data/get_films_data.json").items,
        "genres": GenrePersonItemData.parse_file("tests/data/get_genres_data.json").items,
        "actors": GenrePersonItemData.parse_file("tests/data/get_actors_data.json").items,
        "writers": GenrePersonItemData.parse_file("tests/data/get_writers_data.json").items,
        "directors": GenrePersonItemData.parse_file("tests/data/get_directors_data.json").items,
    }
    return router_schema[router_type]


def get_search_mock():
    return SearchItemData.parse_file("tests/data/get_search_data.json").items
