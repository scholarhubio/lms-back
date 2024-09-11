from fastapi import APIRouter
from .course import router as course_router
from .auth import router as auth_router
from .module import router as module_router
from .unit import router as unit_router
from .task import router as task_router
from .user_answer import router as answer_router


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(course_router, tags=['endpoints for courses'])
v1_router.include_router(auth_router, tags=['auth based endpoints'])
v1_router.include_router(module_router, tags=['endpoints for modules'])
v1_router.include_router(unit_router, tags=['endpoints for units'])
v1_router.include_router(task_router, tags=['endpoints for tasks'])
v1_router.include_router(answer_router, tags=['endpoints for user answers'])
