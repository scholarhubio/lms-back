from .factories import SubscriptionFactory, AccessPeriodFactory, TransactionFactory
from .strategies import FullCoursePaymentStrategy, IncrementalPaymentStrategy
from .utils.payment_calculator import PaymentCalculator
from payments.models import Payment, Subscription


class PaymentService:
    """Facade for handling payment processing and access management."""

    def __init__(self, payment: Payment) -> None:
        self.payment = payment
        self.payment_calculator = PaymentCalculator(self.payment)
        self.payment_strategy = (
            FullCoursePaymentStrategy()
            if self.payment.subscription_plan.is_full_course
            else IncrementalPaymentStrategy(self.payment_calculator)
        )

    def apply_payment(self) -> None:
        """Apply the payment using the selected strategy."""
        subscription: Subscription = SubscriptionFactory.create(self.payment)
        access_manager = AccessPeriodFactory.create_manager(subscription, self.payment)
        self.payment_strategy.process_payment(subscription, access_manager)
        transaction_recorder = TransactionFactory.create_transaction_recorder(self.payment)
        transaction_recorder.record_transaction()
