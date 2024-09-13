from fastapi import APIRouter, Depends
from services.course import get_course_service, ICourseService
from services.auth import get_current_user
from schemas.course import CourseSchema

router = APIRouter(prefix="/course")


@router.get("")
async def get_courses(
    user=Depends(get_current_user),
    service: ICourseService = Depends(get_course_service)) -> list[CourseSchema]:
    return await service.get_courses()
