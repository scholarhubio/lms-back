from . import BaseSchema
from uuid import UUID


class UserAnswerSchema(BaseSchema):
    answer_text: str
    answer_id: UUID
    is_correct: bool


class AnswerSchema(BaseSchema):
    sign: str
    text: str
    user_answer: UserAnswerSchema | None

class TaskSchema(BaseSchema):
    title: str
    complition: str | None = None
    stars: int | None = None
    type: str | None = None
    order: int | None = None


class TaskWithAnswersSchema(TaskSchema):
    answers: list[AnswerSchema]
