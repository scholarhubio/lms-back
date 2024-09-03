from django.db import models
import uuid
from django.utils.text import slugify
from courses.choices import TaskCompletionType, TaskResultType


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDMixin, TimeStampMixin):
    class Meta:
        abstract = True


class ContentBaseModel(UUIDMixin, TimeStampMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    order = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self._state.adding:  # Check if this is a new instance
            # Set the order based on the highest existing order value in the same context
            max_order = self.__class__.objects.filter(**self.get_ordering_scope()).aggregate(
                max_order=models.Max('order')
            )['max_order']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    def get_ordering_scope(self):
        """
        Returns a dictionary representing the scope within which the order should be unique.
        Override this in subclasses to set the ordering scope, e.g., by course or other related objects.
        """
        return {}

    class Meta:
        ordering = ['order']
        abstract = True


class BaseContentSessionModel(BaseModel):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True)
    stars = models.PositiveSmallIntegerField(default=0)
    complition = models.CharField(choices=TaskCompletionType.choices)
    result = models.CharField(choices=TaskResultType.choices)

    class Meta:
        ordering = ['started_at']
        abstract = True
