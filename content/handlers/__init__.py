from .auth_jwt import handler as auth_exc_handler
from fastapi import FastAPI
from async_fastapi_jwt_auth.exceptions import AuthJWTException


def setup_handlers(app: FastAPI):
    app.add_exception_handler(AuthJWTException, auth_exc_handler)
