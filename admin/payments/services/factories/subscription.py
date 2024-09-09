from django.utils import timezone
from payments.models import Subscription, Payment


class SubscriptionFactory:
    """Factory for creating or retrieving subscriptions."""

    @staticmethod
    def create(payment: Payment) -> Subscription:
        """Create or retrieve a subscription for the payment.

        Args:
            payment (Payment): The payment object used to create or retrieve a subscription.

        Returns:
            Subscription: The created or retrieved subscription.
        """
        subscription, _ = Subscription.objects.get_or_create(
            student=payment.student,
            course=payment.course,
            defaults={
                'subscription_plan': payment.subscription_plan,
                'end_date': (
                    payment.course.get_course_end_date()
                    if payment.subscription_plan.is_full_course
                    else timezone.now()
                )
            }
        )
        return subscription
