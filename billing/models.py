from django.db import models
from django.conf import settings


class Subscription(models.Model):
    """
    Stores the Stripe subscription details for a single user.

    This will:
    - track whether they are in a free trial or active paid plan
    - store the related Stripe IDs
    - know when their trial/period ends, so I can gatekeep features
    """

    STATUS_CHOICES = [
        ("trialing", "Trialing"),
        ("active", "Active"),
        ("past_due", "Past due"),
        ("canceled", "Canceled"),
        ("incomplete", "Incomplete"),
        ("incomplete_expired", "Incomplete (expired)"),
        ("unpaid", "Unpaid"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    # Stripe identifiers
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe Customer ID (cus_...)",
    )
    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe Subscription ID (sub_...)",
    )

    # Billing status
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default="trialing",
        help_text="Current status as reported by Stripe.",
    )

    # Dates from Stripe (all in UTC)
    trial_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text="End of free trial period, if any.",
    )
    current_period_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text="End of current billing period.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription for {self.user.username} ({self.status})"
