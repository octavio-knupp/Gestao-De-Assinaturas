from django.db import models
from subscriptions.models import Subscription


class Payment(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('paid', 'Paid'),
            ('pending', 'Pending'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    stripe_checkout_session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    payment_method = models.CharField(
        max_length=50,
        default='stripe'
    )

    def __str__(self):
        return f"Payment {self.id} - {self.status}"