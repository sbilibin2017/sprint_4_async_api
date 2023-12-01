from uuid import UUID

from pydantic import BaseModel


class DataMixin(BaseModel):
    id: UUID
    name: str
