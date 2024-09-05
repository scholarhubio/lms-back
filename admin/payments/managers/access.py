from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from payments.models import AccessPeriod, Subscription, Course
from users.models import Student

class FullCourseAccessManager:
    """Manager for handling full course access."""

    def __init__(
        self, 
        subscription: Subscription, 
        course: Course, 
        access_period_manager: "AccessPeriodManager"
    ) -> None:
        self.subscription = subscription
        self.course = course
        self.access_period_manager = access_period_manager

    def create_access(self) -> None:
        """Create access for the full duration of the course."""
        access_start_date = timezone.now()
        access_end_date = self.course.get_course_end_date()

        self._update_subscription_end_date(access_end_date)
        self.access_period_manager.create_access_period(
            student=self.subscription.student,
            course=self.course,
            start_date=access_start_date,
            end_date=access_end_date
        )

    def _update_subscription_end_date(self, end_date: datetime) -> None:
        """Update the subscription end date.

        Args:
            end_date (datetime): The new end date for the subscription.
        """
        try:
            self.subscription.end_date = end_date
            self.subscription.save()
        except Exception as e:
            # Log the error here
            print(f"Failed to update subscription end date: {e}")


class IncrementalAccessManager:
    """Manager for handling incremental access based on payments."""

    def __init__(
        self, 
        subscription: Subscription, 
        course: Course, 
        access_period_manager: "AccessPeriodManager"
    ) -> None:
        self.subscription = subscription
        self.course = course
        self.access_period_manager = access_period_manager

    def create_access(self, months_paid: int, extra_days: int) -> None:
        """Create access based on incremental payments.

        Args:
            months_paid (int): Number of months covered by the payment.
            extra_days (int): Additional days covered by the payment.
        """
        access_start_date = timezone.now()
        access_end_date = self._calculate_access_end_date(access_start_date, months_paid, extra_days)
        self._extend_subscription(months_paid, extra_days)

        self.access_period_manager.create_access_period(
            student=self.subscription.student,
            course=self.course,
            start_date=access_start_date,
            end_date=access_end_date
        )

    def _calculate_access_end_date(self, start_date: datetime, months_paid: int, extra_days: int) -> datetime:
        """Calculate the access end date based on payments and course limits.

        Args:
            start_date (datetime): The start date of the access period.
            months_paid (int): Number of months covered by the payment.
            extra_days (int): Additional days covered by the payment.

        Returns:
            datetime: The calculated end date, limited by the course's end date.
        """
        calculated_end_date = start_date + relativedelta(months=months_paid) + timedelta(days=extra_days)
        course_end_date = self.course.get_course_end_date()
        return min(calculated_end_date, course_end_date)

    def _extend_subscription(self, months: int, days: int) -> None:
        """Extend the subscription period.

        Args:
            months (int): Number of months to extend.
            days (int): Number of days to extend.
        """
        try:
            self.subscription.extend_subscription(months=months, days=days)
            self.subscription.save()
        except Exception as e:
            # Log the error here
            print(f"Failed to extend subscription: {e}")


class AccessPeriodManager:
    """Manager for creating access periods."""

    def create_access_period(
        self,
        student: Student,
        course: Course,
        start_date: datetime,
        end_date: datetime
    ) -> None:
        """Create an access period for the student to access the course.

        Args:
            student (Student): The student object.
            course (Course): The course object.
            start_date (datetime): The start date of the access period.
            end_date (datetime): The end date of the access period.
        """
        try:
            AccessPeriod.objects.create(
                student=student,
                course=course,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            # Log the error here
            print(f"Failed to create access period: {e}")
