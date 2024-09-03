from django.db import models


class ItemType(models.TextChoices):
    theory = 'theory', "Theory"
    soultion = "solution", "Solution"
    example = "example", "Example"


class TaskType(models.TextChoices):
    single_choice = "single choice", "Single Choice"
    multiple_choices = "multiple choices", "Single Choices"
    single_word = "single word", "Single Word"
    multiple_words = "multiple words", "multiple Words"


class TaskResultType(models.TextChoices):
    passed = 'passed', 'Task passed'
    failed = 'failed', 'Task failed'
    passed_with_teacher = 'passed with teacher', 'Passed with Teacher'


class TaskCompletionType(models.TextChoices):
    started = 'started', 'Started'
    complited = 'complited', 'Complited'


class UnitType(models.TextChoices):
    free = "free", "Free"
    paid = "paid", "Paid"
