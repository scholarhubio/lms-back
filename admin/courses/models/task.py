from django.db import models
from config.models import ContentBaseModel, OrderedModel, BaseModel
from courses.choices import TaskType, ItemType
from ckeditor.fields import RichTextField


class Task(ContentBaseModel, OrderedModel):
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               verbose_name="Родитель",
                               blank=True, null=True, default=None,
                               related_name='children')
    unit = models.ForeignKey('courses.Unit', on_delete=models.CASCADE)
    text = RichTextField()
    type = models.CharField(max_length=25, choices=TaskType.choices, default=TaskType.single_choice)
    order = models.PositiveIntegerField(blank=True)

    class Meta:
        unique_together = ['unit', 'parent', 'order']


class TaskItem(BaseModel):
    task = models.ForeignKey('courses.Task', on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    type = models.CharField(choices=ItemType.choices)


class Answer(BaseModel):
    sign = models.CharField(max_length=10)
    task = models.ForeignKey('courses.Task', on_delete=models.CASCADE)
    text = RichTextField()
    is_correct = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
