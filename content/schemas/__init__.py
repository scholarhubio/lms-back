from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BaseSchema(BaseModel):
    id: UUID

    class Config:
        from_attrbutes = True


class BaseSessionSchema(BaseModel):
    complition: str | None
    user_id: UUID
    started_at: datetime | None = None
    finished_at: datetime | None = None
    stars: int | None
    result: str | None
