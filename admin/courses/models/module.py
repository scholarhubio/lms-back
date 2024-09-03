from django.db import models
from config.models import ContentBaseModel
from courses.choices import UnitType


class Module(ContentBaseModel):
    courses = models.ManyToManyField('courses.Course' ,through="courses.CourseModule")


class Unit(ContentBaseModel):
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)
    type = models.CharField(choices=UnitType.choices, default=UnitType.paid.value)


class UnitItem(ContentBaseModel):
    unit = models.OneToOneField('courses.Unit', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
