from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from payments.models import AccessPeriod


class AccessService:
    def __init__(self, payment):
        self.payment = payment

    def create_full_course_access(self, subscription):
        """Create access for the full duration of the course."""
        access_start_date = timezone.now()
        access_end_date = self.payment.course.get_course_end_date()
        subscription.end_date = access_end_date
        subscription.save()
        AccessPeriodManager.create_access_period(self.payment.student, self.payment.course, access_start_date, access_end_date)

    def create_incremental_access(self, subscription, months_paid, extra_days):
        """Create access based on incremental payments."""
        access_start_date = timezone.now()
        access_end_date = access_start_date + relativedelta(months=months_paid) + timedelta(days=extra_days)
        course_end_date = self.payment.course.get_course_end_date()
        access_end_date = min(access_end_date, course_end_date)  # Ensure it does not exceed the course end date

        subscription.extend_subscription(months=months_paid, days=extra_days)
        AccessPeriodManager.create_access_period(self.payment.student, self.payment.course, access_start_date, access_end_date)


class AccessPeriodManager:
    @staticmethod
    def create_access_period(student, course, start_date, end_date):
        """Create an access period for the student to access the course."""
        AccessPeriod.objects.create(
            student=student,
            course=course,
            start_date=start_date,
            end_date=end_date
        )
