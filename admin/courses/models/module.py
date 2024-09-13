from django.db import models
from config.models import ContentBaseModel, OrderedModel
from courses.choices import UnitType


class Module(ContentBaseModel):
    courses = models.ManyToManyField('courses.Course' ,through="courses.CourseModule")

    def __str__(self):
        return self.title


class Unit(ContentBaseModel, OrderedModel):
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)
    description = models.TextField()
    type = models.CharField(choices=UnitType.choices, default=UnitType.paid.value)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['module', 'order']
        unique_together = ['module', 'order']
    
    def __str__(self):
        return self.title


class UnitItem(ContentBaseModel):
    unit = models.OneToOneField('courses.Unit', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
