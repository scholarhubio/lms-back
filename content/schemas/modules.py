from . import BaseSchema, BaseSessionSchema
from datetime import datetime
from uuid import UUID


class ModuleSession(BaseSessionSchema):
    pass



class ModuleSchema(BaseSchema):
    title: str
    sessions: list[ModuleSession] | None = None
