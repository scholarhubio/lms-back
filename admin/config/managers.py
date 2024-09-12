from django.db import models


class ActiveManager(models.Manager):
    """Manager to filter out objects marked as deleted."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """Custom manager to exclude soft-deleted records."""
    def get_queryset(self):
        # Exclude records where is_deleted is True
        return super().get_queryset().filter(is_deleted=False)
