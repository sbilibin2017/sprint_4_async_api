from pydantic import BaseModel


class GenrePersonDetailSchema(BaseModel):
    id: str
    name: str
    film: list[dict]
