from fastapi import APIRouter, Depends
from services.unit import get_unit_service, IUnitService
from uuid import UUID
from schemas.unit import UnitSchema


router = APIRouter(prefix="/units")


@router.get("")
async def get_units(
    module_id: UUID,
    service: IUnitService = Depends(get_unit_service),
    ) -> list[UnitSchema]:
    return await service.get_units(module_id=module_id)
