from django.utils import timezone
from billing.models import Subscription


def plan_status(request):
    """
    Adds current account plan info to all templates.
    Used for the small banner under the navbar.
    """

    # Only show plan info to authenticated users
    if not request.user.is_authenticated:
        return {}

    # Each user has at most one subscription (OneToOne)
    sub = Subscription.objects.filter(user=request.user).first()

    now = timezone.now()

    # Default state
    label = "Free plan"
    badge = "free"

    if sub:
        status = getattr(sub, "status", "")

        # Trial still active
        if sub.trial_end and sub.trial_end > now:
            label = "Regulate+ free trial"
            badge = "trial"

        # Stripe trial status
        elif status == "trialing":
            label = "Regulate+ free trial"
            badge = "trial"

        # Paid subscription
        elif status == "active":
            label = "Regulate+ subscription"
            badge = "plus"

        # Subscription scheduled to end
        elif sub.current_period_end and sub.current_period_end > now:
            label = "Regulate+ (ending soon)"
            badge = "ending"

    return {
        "plan_status": {
            "label": label,
            "badge": badge,
        }
    }
