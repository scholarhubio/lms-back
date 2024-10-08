from fastapi import APIRouter, FastAPI
from .v1 import v1_router

api_router = APIRouter(prefix='/api')
api_router.include_router(v1_router)


def setup_routers(app: FastAPI):
    root_router = APIRouter()
    root_router.include_router(api_router)
    app.include_router(root_router)
