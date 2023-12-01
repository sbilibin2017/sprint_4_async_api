from pydantic import BaseModel


class FilmDetailSchema(BaseModel):
    id: str
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
