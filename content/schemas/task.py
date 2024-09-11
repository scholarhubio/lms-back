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
    stars: int = None
    type: str
    order: int


class TaskWithAnswersSchema(TaskSchema):
    answers: list[AnswerSchema]
