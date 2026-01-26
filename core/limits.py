from django.utils import timezone

from billing.models import Subscription
from .models import Entry


# Free plan entry cap
FREE_ENTRY_LIMIT = 10

# Subscription statuses treated as paid access
PAID_STATUSES = {"trialing", "active"}


def get_subscription(user):
    """Return the user's Subscription, or None."""
    if not user or not user.is_authenticated:
        return None
    return Subscription.objects.filter(user=user).first()


def has_paid_access(subscription):
    """
    Return True if the user should be treated as Regulate+.
    Includes active/trialing subscriptions and grace periods.
    """
    if not subscription:
        return False

    if subscription.status in PAID_STATUSES:
        return True

    # Grace period: canceled but access period not yet ended
    if (
        subscription.status == "canceled"
        and subscription.current_period_end
        and subscription.current_period_end > timezone.now()
    ):
        return True

    return False


def user_entry_count(user):
    """Return total entry count for a user."""
    if not user or not user.is_authenticated:
        return 0
    return Entry.objects.filter(user=user).count()


def is_free_locked(user):
    """
    Return True if a free user has reached the entry limit.
    Locked users can view entries but cannot create or modify them.
    """
    subscription = get_subscription(user)

    if has_paid_access(subscription):
        return False

    return user_entry_count(user) >= FREE_ENTRY_LIMIT
