import orjson
from pydantic import BaseModel
from utils.mixin import DataMixin
from utils.orjson import orjson_dumps


class Film(BaseModel):
    id: str
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: list[str]
    actors_names: list[str]
    actors: list[DataMixin]
    writers_names: list[str]
    writers: list[DataMixin]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
