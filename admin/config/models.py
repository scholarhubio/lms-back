from django.db import models
from courses.choices import TaskCompletionType, TaskResultType
import uuid
from config.managers import ActiveManager, SoftDeleteManager


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)

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

    objects = SoftDeleteManager()  # Default manager
    active_objects = ActiveManager()  # Custom manager to filter out deleted objects

    def delete(self, using=None, keep_parents=False):
        """Soft delete the object by setting `is_deleted` to True."""
        self.is_deleted = True
        self.save()


class ContentBaseModel(UUIDMixin, TimeStampMixin):
    title = models.CharField(max_length=255)
    
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
    user_id = models.UUIDField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    stars = models.PositiveSmallIntegerField(default=0)
    complition = models.CharField(choices=TaskCompletionType.choices, default=TaskCompletionType.started)
    result = models.CharField(choices=TaskResultType.choices, null=True)
    tries = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['started_at']
        abstract = True
