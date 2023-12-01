from datetime import datetime

from pydantic import BaseModel


class PostgresPydantic(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


class EsPydantic(BaseModel):
    host: str
    port: int


class RedisPydantic(BaseModel):
    host: str
    port: int


class FilmIndexData(BaseModel):
    id: str
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: list[str]
    actors_names: list[str]
    actors: list[dict]
    writers_names: list[str]
    writers: list[dict]


class Mixin(BaseModel):
    id: str
    name: str


class GenreIndexData(Mixin):
    pass


class PersonIndexData(Mixin):
    pass


class GenreWithFilmIndexData(Mixin):
    film: list[dict]


class PersonWithFilmIndexData(Mixin):
    film: list[dict]


class FilmworkPydantic(BaseModel):
    id: str
    rating: float
    title: str
    description: str
    updated_at: datetime


class FilmworkGenrePydantic(BaseModel):
    filmwork_id: str
    genre_id: str
    name: str
    description: str


class FilmworkPersonPydantic(BaseModel):
    filmwork_id: str
    person_id: str
    full_name: str
    role: str
