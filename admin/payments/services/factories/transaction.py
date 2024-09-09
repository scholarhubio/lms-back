from payments.models import Transaction, Payment
from payments.choices import TransactionType


class TransactionRecorder:
    """Recorder for transactions related to payments."""

    def __init__(self, payment: Payment) -> None:
        self.payment = payment

    def record_transaction(self) -> None:
        """Record the payment as a transaction."""
        Transaction.objects.create(
            student=self.payment.student,
            transaction_type=TransactionType.DEBIT,
            amount=self.payment.amount,
            description=self._generate_description()
        )

    def _generate_description(self) -> str:
        """Generate a description for the transaction.

        Returns:
            str: Description of the transaction.
        """
        return f"Paid for {self.payment.subscription_plan.title} of {self.payment.course.title}"


class TransactionFactory:
    """Factory for creating transaction recorders."""

    @staticmethod
    def create_transaction_recorder(payment: Payment) -> TransactionRecorder:
        """Create a transaction recorder.

        Args:
            payment (Payment): The payment object.

        Returns:
            TransactionRecorder: An instance of the TransactionRecorder.
        """
        return TransactionRecorder(payment)
