from datetime import timezone
from payments.models import Subscription, Payment


class SubscriptionService:
    def __init__(self, payment: Payment):
        self.payment: Payment = payment

    def get_or_create_subscription(self):
        """Retrieve or create a subscription for the student and course."""
        subscription, _ = Subscription.objects.get_or_create(
            student=self.payment.student,
            course=self.payment.course,
            defaults={
                'subscription_plan': self.payment.subscription_plan,
                'end_date': self.payment.course.get_course_end_date() if self.payment.subscription_plan.is_full_course else timezone.now()
            }
        )
        return subscription
