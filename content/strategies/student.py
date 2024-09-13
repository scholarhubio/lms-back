from models.courses import UserModuleSession, UserUnitSession
from models import User, Answer
from models.courses.moduls import Course, CourseModule, Module, Unit, Task
from models.courses.result import UserAnswer, UserTaskSession
from models.courses import Answer
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from uuid import UUID
from interfaces.strategy import IQueryStrategy
from models.payments.models import Subscription
from datetime import date


class StudentQueryStrategy(IQueryStrategy):
    async def get_task_by_answer(self, answer_id: UUID) -> Task:
        return select(
            Task).join(
                Answer).where(
                    Answer.id == answer_id)

    async def get_courses(self, user: User) -> list[Course]:
        return select(Course).join_from(
            CourseModule,
            Subscription.course_module==CourseModule.id
            ).where(
                Subscription.is_active == True,
                Subscription.user_id == user.id,
                Subscription.start_date >= date.today(),
                Subscription.end_date <= date.today(),
                ).order_by(desc(CourseModule.order))

    async def get_modules(self, course_id: UUID, user_id: UUID) -> list[Course]:
        return select(
            Module
            ).join(
                CourseModule,
                CourseModule.module_id == Module.id).where(
                    CourseModule.course_id == course_id,
                    ).order_by(CourseModule.order)

    async def get_units(self, module_id: UUID) -> list[Course]:
        return select(
            Unit).options(selectinload(Unit.tasks)).where(
                Unit.module_id == module_id).order_by(Unit.order)

    async def get_task_highest_parent(self, task_id: UUID) -> Task:
        task_cte = (
            select(Task.id, Task.parent_id)
            .where(Task.id == task_id)
            .cte(name="task_hierarchy", recursive=True)
        )
        recursive_part = (
            select(Task.id, Task.parent_id)
            .join(task_cte, Task.id == task_cte.c.parent_id)
        )
        task_cte = task_cte.union_all(recursive_part)
        query = select(
            Task
            ).join(
                task_cte, Task.id == task_cte.c.id
                ).where(
                    task_cte.c.parent_id == None)
        return query

    async def get_tasks(self, unit_id: UUID) -> list[Task]:
        return select(
            Task).options(selectinload(Task.answers)).where(
                Task.unit_id == unit_id).order_by(Task.order)

    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        return select(
            UserModuleSession).where(
                UserModuleSession.module_id == module_id,
                UserModuleSession.user_id == user_id).order_by(
                    UserModuleSession.created_at)

    async def get_user_unit_session(self, unit_id: UUID, user_id: UUID) -> UserUnitSession:
        return select(
            UserUnitSession).where(
                UserUnitSession.unit_id == unit_id,
                UserUnitSession.user_id == user_id).order_by(
                    UserUnitSession.created_at)

    async def get_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        return select(
            UserTaskSession).where(
                UserTaskSession.user_id == user_id,
                UserTaskSession.task_id == task_id).order_by(UserTaskSession.created_at)

    async def module_unit_task_by_answer(self, answer_id: UUID, user_id: UUID):
        return select(
            UserModuleSession.id.label('module_id'),
            UserUnitSession.id.label('unit_id'),
            UserTaskSession.id.label('task_id'),
            ).select_from(
                UserAnswer
                ).join(
                    UserTaskSession,
                    UserAnswer.session_id == UserTaskSession.id).join(
                        UserUnitSession,
                        UserUnitSession.user_id == UserTaskSession.user_id, isouter=True).join(
                            UserModuleSession, UserModuleSession.user_id == UserTaskSession.user_id, isouter=True).where(
                                UserAnswer.answer_id == answer_id,
                                UserAnswer.user_id == user_id)

    async def start_user_module_session(
            self, module_id: UUID,
            tries: int, user_id: UUID,
            ) -> UserModuleSession:
        return UserModuleSession(
            module_id=module_id,
            tries=tries,
            user_id=user_id
            )

    async def start_user_unit_session(
            self, unit_id: UUID,
            tries: int, user_id: UUID,
            ) -> UserUnitSession:
        return UserUnitSession(
            unit_id=unit_id,
            tries=tries,
            user_id=user_id
            )

    async def start_user_task_session(
            self, task_id: UUID,
            tries: int, user_id: UUID,
            ) -> UserTaskSession:
        return UserTaskSession(
            task_id=task_id,
            tries=tries,
            user_id=user_id
            )

    async def create_user_answer(
            self, answer_id: UUID,
            user_id: UUID, session_id: UUID,
            is_correct: bool, answer_text: str
            ) -> bool:
        return UserAnswer(
            session_id=session_id,
            answer_id=answer_id,
            user_id=user_id,
            is_correct=is_correct,
            answer_text=answer_text
            )

    async def get_answer(self, answer_id: UUID) -> UserAnswer:
        return select(Answer).where(Answer.id == answer_id)

    async def get_user_answer(self, answer_id: UUID, session_id: UUID, task_id: UUID) -> UserAnswer:
        pass

    async def create_user_model_session(self, module_id: UUID, user_id: UUID):
        return UserModuleSession(
            module_id=module_id,
            user_id=user_id,
        )
    
    async def get_task(self, task_id: UUID) -> Task:
        return select(
            Task).options(selectinload(
                Task.answers).options(selectinload(Answer.user_answer))).where(Task.id == task_id)


def get_student_strategy() -> StudentQueryStrategy:
    return StudentQueryStrategy()
