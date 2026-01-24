from django.db import models
from django.conf import settings


class Subscription(models.Model):
    """
    Stores Stripe subscription details for a single user.
    Tracks trial/active state and important end dates for gating features.
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

    # Trial history flag (trial only once)
    has_had_trial = models.BooleanField(
        default=False,
        help_text="True if the user has ever started a free trial.",
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

    # Billing status (default should be neutral until Stripe tells us)
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default="incomplete",
        help_text="Current status as reported by Stripe.",
    )

    # Dates from Stripe (UTC)
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
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text="True if the user has cancelled and the subscription will end at period end/trial end.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription for {self.user.username} ({self.status})"
