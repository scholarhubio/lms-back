from django.db import models


class RoleType(models.TextChoices):
    CEO = 'ceo', 'Chief Executive Officer'
    SALE_MANAGER = 'sale_manager', 'Sale Manager'
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'
    SALE_LEAD = 'sale_lead', 'Sale Team Lead'
    SALE_HEAD = 'sale_head', 'Sale Department Head'
