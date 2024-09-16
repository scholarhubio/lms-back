from . import BaseSchema, BaseSessionSchema
from uuid import UUID
from .task import PureTaskSchema


class UnitSession(BaseSessionSchema):
    pass


class UnitSchema(BaseSchema):
    description: str | None = None
    order: int
    title: str | None = None
    module_id: UUID
    sessions: list[UnitSession] | None = None
    tasks: list[PureTaskSchema] | None = None
