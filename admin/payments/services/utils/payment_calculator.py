from payments.models import Payment


class PaymentCalculator:
    """Utility for calculating the months and days covered by the payment."""

    def __init__(self, payment: Payment) -> None:
        self.payment = payment

    def calculate_months_and_days_paid(self) -> tuple[int, int]:
        """Calculate the number of months and extra days covered by the amount paid.

        Returns:
            tuple[int, int]: Number of months paid and extra days covered.
        """
        price_per_month = self.payment.subscription_plan.price / self.payment.subscription_plan.duration_in_months
        price_per_day = price_per_month / 30  # Approximate price per day
        total_days_paid = self.payment.amount / price_per_day
        months_paid = int(total_days_paid // 30)
        extra_days = int(total_days_paid % 30)
        return months_paid, extra_days
