from pydantic import BaseModel


class UserSignIn(BaseModel):
    access_token: str
    refresh_token: str
