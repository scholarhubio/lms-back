from django.db import models
from config.models import BaseModel, BaseContentSessionModel


class UserAnswer(BaseModel):
    user_id = models.UUIDField()
    session = models.ForeignKey('courses.UserTaskSession', on_delete=models.SET_NULL, null=True)
    answer = models.OneToOneField('courses.Answer', on_delete=models.SET_NULL, null=True)
    answer_text = models.TextField()
    is_correct = models.BooleanField()


class UserTaskSession(BaseContentSessionModel):
    task = models.ForeignKey('courses.Task', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return str(self.id)


class UserUnitSession(BaseContentSessionModel):
    unit = models.ForeignKey('courses.Unit', on_delete=models.SET_NULL, null=True)


class UserModuleSession(BaseContentSessionModel):
    module = models.ForeignKey('courses.Module', on_delete=models.SET_NULL, null=True)
