from fastapi import APIRouter, Depends
from services.module import get_module_service, IModuleService
from uuid import UUID


router = APIRouter(prefix="/module")


@router.get("")
async def get_modules(
    course_id: UUID,
    service: IModuleService = Depends(get_module_service),
    ):
    return await service.get_modules(course_id=course_id)
