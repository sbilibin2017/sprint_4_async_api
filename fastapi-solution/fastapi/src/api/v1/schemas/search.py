from pydantic import BaseModel


class SearchDetailSchema(BaseModel):
    title: str
    description: str
    imdb_rating: float
