from fastapi import APIRouter, Depends
from services.unit import get_unit_service, IUnitService
from uuid import UUID


router = APIRouter(prefix="/units")


@router.get("")
async def get_units(
    module_id: UUID,
    service: IUnitService = Depends(get_unit_service),
    ):
    return await service.get_units(module_id=module_id)
