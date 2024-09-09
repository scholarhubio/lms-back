from fastapi import APIRouter
from .course import router as course_router
from .auth import router as auth_router
v1_router = APIRouter(prefix='/v1')
v1_router.include_router(course_router)
v1_router.include_router(auth_router)
