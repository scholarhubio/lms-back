from payments.managers.access import FullCourseAccessManager, IncrementalAccessManager
from payments.models import Subscription, Payment


class AccessPeriodFactory:
    """Factory for creating access managers based on payment type."""

    @staticmethod
    def create_manager(subscription: Subscription, payment: Payment) -> object:
        """Create an appropriate access manager based on the payment type.

        Args:
            subscription (Subscription): The subscription object.
            payment (Payment): The payment object.

        Returns:
            object: The access manager instance for handling access creation.
        """
        if payment.subscription_plan.is_full_course:
            return FullCourseAccessManager(subscription, payment.course)
        return IncrementalAccessManager(subscription, payment.course)
