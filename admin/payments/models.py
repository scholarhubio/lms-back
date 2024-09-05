from django.db import models
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from users.models import Student
from courses.models import Course
from config.models import BaseModel
from payments.choices import TransactionType


class SubscriptionPlan(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration_in_months = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_full_course = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.duration_in_months} months)"


class Subscription(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title} ({self.subscription_plan.title})"


class AccessPeriod(BaseModel):
    """Model to represent access granted for a specific period based on payments."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Access for {self.student.user.username} to {self.course.title} from {self.start_date} to {self.end_date}"


class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment by {self.student.user.username} for {self.course.title} ({self.subscription_plan.title})"


class Transaction(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=TransactionType.choices)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.type} for {self.student.user.username} - {self.amount} on {self.date}"
