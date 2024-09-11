from api import setup_routers
from handlers import setup_handlers
from fastapi import FastAPI
from fastapi.responses import  ORJSONResponse
from fastapi_pagination import add_pagination
from lifespan import setup_lifespan
from core import settings
from schemas.auth import AuthSettingsSchema
from async_fastapi_jwt_auth import AuthJWT
from db.redis import get_redis
from exceptions import TokenDenied
from core.logger import LOGGING
from logging import config as logging_config

logging_config.dictConfig(LOGGING)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description="Auth logic",
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        lifespan=setup_lifespan
    )
    setup_handlers(app)
    #setup_middleware(app)
    setup_routers(app)
    add_pagination(app)
    return app

app = create_app()

@AuthJWT.load_config
def get_config():
    return AuthSettingsSchema()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(
    decrypted_token):
    cache = await get_redis()
    jti = decrypted_token["jti"]
    entry = await cache.exists(jti)
    if entry == 1:
        raise TokenDenied
    return entry and entry == "true"
