from fastapi import APIRouter, Body, Depends, Header
from services.course import get_course_service, ICourseService
from services.auth import get_current_user

router = APIRouter(prefix="/course")


@router.get("/")
async def get_courses(
    user=Depends(get_current_user),
    service: ICourseService = Depends(get_course_service)):
    print(user, '#########')
    return await service.get_courses()
