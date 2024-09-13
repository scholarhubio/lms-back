from django.db import models
from users.models import User
from courses.models import CourseModule
from config.models import BaseModel
from payments.choices import TransactionType
from datetime import date


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.phone_number}: from {self.start_date} to {self.end_date}"


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=TransactionType.choices)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.type} for {self.user.username} - {self.amount} on {self.date}"
