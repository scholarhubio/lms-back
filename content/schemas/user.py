from pydantic import BaseModel


class UserSchema(BaseModel):
    role: str
