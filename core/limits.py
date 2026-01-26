# core/limits.py
from django.utils import timezone

from billing.models import Subscription
from .models import Entry

FREE_ENTRY_LIMIT = 10
PAID_STATUSES = {"trialing", "active"}


def get_subscription(user):
    """Return the user's Subscription or None."""
    if not user or not user.is_authenticated:
        return None
    return Subscription.objects.filter(user=user).first()


def has_paid_access(subscription):
    """
    True if the user should be treated as Regulate+ (trialing/active),
    or still within a paid/grace period window.
    """
    if not subscription:
        return False

    if subscription.status in PAID_STATUSES:
        return True

    # Grace period: canceled but current period not ended yet
    if (
        subscription.status == "canceled"
        and subscription.current_period_end
        and subscription.current_period_end > timezone.now()
    ):
        return True

    return False


def user_entry_count(user):
    """Total entries for this user."""
    if not user or not user.is_authenticated:
        return 0
    return Entry.objects.filter(user=user).count()


def is_free_locked(user):
    """
    Free users: once they have 10 entries total, they become view-only.
    - can still view entries
    - cannot create new entries
    - cannot edit/delete entries
    """
    subscription = get_subscription(user)
    if has_paid_access(subscription):
        return False

    return user_entry_count(user) >= FREE_ENTRY_LIMIT
