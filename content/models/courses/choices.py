from enum import Enum


class ItemType(Enum):
    THEORY = "theory"
    SOLUTION = "solution"
    EXAMPLE = "example"

    def __str__(self):
        return self.name.capitalize()


class TaskType(Enum):
    SINGLE_CHOICE = "single choice"
    MULTIPLE_CHOICES = "multiple choices"
    SINGLE_WORD = "single word"
    MULTIPLE_WORDS = "multiple words"

    def __str__(self):
        return self.name.replace('_', ' ').capitalize()


class TaskResultType(Enum):
    PASSED = "passed"
    FAILED = "failed"
    PASSED_WITH_TEACHER = "passed with teacher"

    def __str__(self):
        return self.name.replace('_', ' ').capitalize()


class TaskCompletionType(Enum):
    STARTED = "started"
    COMPLETED = "completed"

    def __str__(self):
        return self.name.capitalize()


class UnitType(Enum):
    FREE = "free"
    PAID = "paid"

    def __str__(self):
        return self.name.capitalize()