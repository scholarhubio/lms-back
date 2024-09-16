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


class TaskItem(BaseSchema):
    link: str | None
    type: str


class TaskSchema(BaseSchema):
    title: str
    complition: str | None = None
    stars: int | None = None
    type: str | None = None
    order: int | None = None
    items: list[TaskItem] | None = None


class TaskWithAnswersSchema(TaskSchema):
    answers: list[AnswerSchema]


class PureTaskSchema(BaseSchema):
    title: str
    text: str
    order: int
    unit_id: UUID
    type: str
