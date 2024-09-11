from fastapi import APIRouter, Depends
from services.task import get_task_service, ITaskService
from uuid import UUID
from schemas.task import TaskSchema, TaskWithAnswersSchema


router = APIRouter(prefix="/tasks")


@router.get("")
async def get_tasks(
    unit_id: UUID,
    service: ITaskService = Depends(get_task_service),
    ) -> list[TaskSchema]:
    return await service.get_tasks(unit_id=unit_id)


@router.get("/{task_id}")
async def get_task(
    task_id: UUID,
    service: ITaskService = Depends(get_task_service)) -> TaskWithAnswersSchema:
    return await service.get_task(task_id=task_id)


@router.post("/{task_id}/session")
async def create_task_session(
    task_id: UUID,
    service: ITaskService = Depends(get_task_service),
    ):
    return await service.create_user_task_session(task_id=task_id)
