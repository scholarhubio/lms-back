from django.db import models


class TransactionType(models.TextChoices):
    DEBIT = 'debit', 'Debit'
    CREDIT = 'credit', 'Credit'
