from pydantic import BaseModel, Field, field_validator


class AnswerResponse(BaseModel):
    detail: str = Field(default="Incorrect")
    is_correct: bool
