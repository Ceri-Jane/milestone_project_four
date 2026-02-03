from django.utils import timezone
from billing.models import Subscription


def plan_status(request):
    """
    Global plan label for the navbar/banner.
    Intentionally minimal: plan type only.
    """
    if not request.user.is_authenticated:
        return {}

    sub = Subscription.objects.filter(user=request.user).first()
    now = timezone.now()

    label = "Free"
    badge = "free"   # optional: for CSS styling

    if sub:
        # Trial (trial_end in future)
        if getattr(sub, "trial_end", None) and sub.trial_end > now:
            label = "Regulate+ (Free Trial)"
            badge = "trial"

        # Active subscription
        elif getattr(sub, "status", "") in ("active", "trialing"):
            label = "Regulate+"
            badge = "plus"

        # Optional: if you have cancel-at-period-end + current_period_end
        elif getattr(sub, "current_period_end", None) and sub.current_period_end > now:
            label = "Regulate+ (Ending Soon)"
            badge = "ending"

    return {
        "plan_status": {
            "label": label,
            "badge": badge,
        }
    }
