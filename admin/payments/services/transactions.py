from payments.models import Transaction, Payment
from payments.choices import TransactionType


class TransactionService:
    def __init__(self, payment: Payment):
        self.payment: Payment = payment

    def record_transaction(self):
        """Record the payment as a transaction."""
        Transaction.objects.create(
            student=self.payment.student,
            transaction_type=TransactionType.DEBIT,
            amount=self.payment.amount,
            description=f"Paid for {self.payment.subscription_plan.title} of {self.payment.course.title}"
        )
