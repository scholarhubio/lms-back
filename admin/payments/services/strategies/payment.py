from payments.models import Subscription
from payments.managers.access import FullCourseAccessManager, IncrementalAccessManager


class FullCoursePaymentStrategy:
    """Strategy for handling full course payments."""

    def process_payment(self, subscription: Subscription, access_manager: FullCourseAccessManager) -> None:
        """Process payment for a full course.

        Args:
            subscription (Subscription): The subscription object.
            access_manager (FullCourseAccessManager): Manager for full course access.
        """
        access_manager.create_access()


class IncrementalPaymentStrategy:
    """Strategy for handling incremental payments."""

    def __init__(self, payment_calculator: object) -> None:
        self.payment_calculator = payment_calculator

    def process_payment(self, subscription: Subscription, access_manager: IncrementalAccessManager) -> None:
        """Process an incremental payment.

        Args:
            subscription (Subscription): The subscription object.
            access_manager (IncrementalAccessManager): Manager for incremental access.
        """
        months_paid, extra_days = self.payment_calculator.calculate_months_and_days_paid()
        access_manager.create_access(months_paid, extra_days)
