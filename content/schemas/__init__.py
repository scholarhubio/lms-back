from pydantic import BaseModel
from uuid import UUID


class BaseSchema(BaseModel):
    id: UUID

    class Config:
        from_attrbutes = True
