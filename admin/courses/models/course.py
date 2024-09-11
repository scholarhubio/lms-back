from django.db import models
from config.models import ContentBaseModel, OrderedModel, BaseModel


class Course(ContentBaseModel):
    lessons_per_day = models.IntegerField(default=1)
    modules = models.ManyToManyField('courses.Module' ,through="courses.CourseModule")


class CourseModule(BaseModel, OrderedModel):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    def get_ordering_scope(self):
        return {
            'course': self.course,
            'module': self.module
            }

    class Meta(OrderedModel.Meta):
        unique_together = ('course', 'module')
        ordering = ['course', 'module', 'order']
