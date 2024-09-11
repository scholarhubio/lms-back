from fastapi import APIRouter, Depends
from services.user_answer import get_user_answer_service, IUserAnswerService
from uuid import UUID
from schemas.responses.user_answer import AnswerResponse


router = APIRouter(prefix="/user_answer")


@router.post("", status_code=201)
async def create_answer(
    answer_id: UUID,
    service: IUserAnswerService = Depends(get_user_answer_service),
    ) -> AnswerResponse:
    return await service.create_user_answer(answer_id=answer_id)
