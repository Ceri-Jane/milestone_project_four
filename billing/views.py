from datetime import datetime, timezone as dt_timezone
import logging

import stripe
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.utils import timezone

from .models import Subscription

# Stripe API configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


def _to_dt(ts):
    """Convert Stripe timestamps to timezone-aware datetimes."""
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


def _stripe_get(obj, key):
    """
    Stripe objects sometimes behave like dicts, sometimes like attribute objects.
    This helper safely supports both.
    """
    if obj is None:
        return None
    try:
        val = obj.get(key)
        if val is not None:
            return val
    except Exception:
        pass
    return getattr(obj, key, None)


def _days_left(dt_value):
    """Return whole days left (ceil-ish), never negative; None if dt_value missing."""
    if not dt_value:
        return None
    now = timezone.now()
    seconds = (dt_value - now).total_seconds()
    if seconds <= 0:
        return 0
    return int((seconds + 86399) // 86400)


def _add_interval(dt_value, interval, interval_count):
    """Add Stripe recurring interval to a datetime (month/year/week/day)."""
    count = int(interval_count or 1)

    if interval == "day":
        return dt_value + relativedelta(days=count)
    if interval == "week":
        return dt_value + relativedelta(weeks=count)
    if interval == "month":
        return dt_value + relativedelta(months=count)
    if interval == "year":
        return dt_value + relativedelta(years=count)

    # Unknown interval – safest: no change
    return dt_value


def _derive_period_end_from_anchor(stripe_sub):
    """
    Stripe sometimes returns current_period_end=None in restricted/test responses.
    We can still derive "next billing date" using:
      - billing_cycle_anchor (timestamp)
      - subscription item price recurring interval (+ interval_count)
    """
    anchor_ts = _stripe_get(stripe_sub, "billing_cycle_anchor")
    if not anchor_ts:
        return None

    anchor_dt = _to_dt(anchor_ts)
    if not anchor_dt:
        return None

    # Pull recurring interval from the first subscription item
    items = _stripe_get(stripe_sub, "items")
    items_data = _stripe_get(items, "data") if items else None
    if not items_data:
        return None

    first_item = items_data[0]
    price = _stripe_get(first_item, "price") or _stripe_get(first_item, "plan")

    recurring = _stripe_get(price, "recurring") if price else None
    interval = _stripe_get(recurring, "interval") if recurring else None
    interval_count = _stripe_get(recurring, "interval_count") if recurring else 1

    if not interval:
        # Some older structures store interval on plan directly
        interval = _stripe_get(price, "interval")
        interval_count = _stripe_get(price, "interval_count") or interval_count

    if not interval:
        return None

    # Next billing date = anchor + interval
    return _add_interval(anchor_dt, interval, interval_count)


def _upsert_subscription(user, stripe_sub, stripe_customer_id=None):
    """Create/update a user's Subscription record from Stripe subscription data."""
    sub_id = _stripe_get(stripe_sub, "id")
    cust_id = stripe_customer_id or _stripe_get(stripe_sub, "customer")
    status = _stripe_get(stripe_sub, "status")

    current_period_end = _to_dt(_stripe_get(stripe_sub, "current_period_end"))
    trial_end = _to_dt(_stripe_get(stripe_sub, "trial_end"))

    obj, _ = Subscription.objects.get_or_create(user=user)

    obj.stripe_subscription_id = sub_id
    obj.stripe_customer_id = cust_id
    obj.status = status or obj.status
    obj.current_period_end = current_period_end
    obj.trial_end = trial_end

    # Mark trial usage once a trial has occurred
    if trial_end or status == "trialing":
        obj.has_had_trial = True

    obj.save()
    return obj


def _checkout_delayed_message(request):
    """Consistent message for the common webhook-delay case (assessor-friendly)."""
    messages.info(
        request,
        "Checkout completed. Your plan usually updates within a few seconds. "
        "If it doesn’t, refresh this page or try again in a minute."
    )


@login_required
def regulate_plus(request):
    """Regulate+ hub page (trial / upgrade / manage billing)."""
    sub = Subscription.objects.filter(user=request.user).first()
    status = getattr(sub, "status", None)

    # Best-effort sync fallback:
    # If user is active/trialing but dates are missing locally, fetch subscription from Stripe,
    # then derive billing date from billing_cycle_anchor if needed.
    if sub and sub.stripe_subscription_id and status in ["trialing", "active"]:
        needs_trial_sync = status == "trialing" and not sub.trial_end
        needs_billing_sync = status == "active" and not sub.current_period_end

        if needs_trial_sync or needs_billing_sync:
            try:
                stripe_sub = stripe.Subscription.retrieve(
                    sub.stripe_subscription_id,
                    expand=["latest_invoice", "customer", "items.data.price"]
                )

                updated = _upsert_subscription(
                    request.user,
                    stripe_sub,
                    stripe_customer_id=getattr(sub, "stripe_customer_id", None),
                )

                # If active but still missing current_period_end, derive from anchor+interval
                if updated.status == "active" and not updated.current_period_end:
                    derived = _derive_period_end_from_anchor(stripe_sub)
                    if derived:
                        updated.current_period_end = derived
                        updated.save(update_fields=["current_period_end"])

                sub = Subscription.objects.filter(user=request.user).first()
                status = getattr(sub, "status", None)

            except Exception:
                logger.exception("Regulate+ sync on page load failed")

    trial_end = getattr(sub, "trial_end", None) if sub else None
    current_period_end = getattr(sub, "current_period_end", None) if sub else None

    context = {
        "subscription": sub,
        "subscription_status": status,
        "is_active_plan": status in ["trialing", "active"],
        "has_had_trial": getattr(sub, "has_had_trial", False),

        "trial_end": trial_end,
        "trial_days_left": _days_left(trial_end),
        "current_period_end": current_period_end,
        "billing_days_left": _days_left(current_period_end),
    }
    return render(request, "billing/regulate_plus.html", context)


@login_required
def start_trial(request):
    sub = Subscription.objects.filter(user=request.user).first()

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("regulate_plus")

    if sub and sub.has_had_trial:
        messages.info(request, "You can only use the free trial once per user.")
        return redirect("regulate_plus")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            metadata={
                "user_id": str(request.user.id),
                "username": request.user.username,
                "email": request.user.email,
            },
            subscription_data={
                "trial_period_days": 5,
                "metadata": {
                    "user_id": str(request.user.id),
                    "username": request.user.username,
                    "email": request.user.email,
                },
            },
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(
                reverse("checkout_success")
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("checkout_cancelled")),
        )
        return redirect(session.url)

    except Exception:
        logger.exception("Stripe Checkout Error (trial)")
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("regulate_plus")


@login_required
def start_subscription(request):
    sub = Subscription.objects.filter(user=request.user).first()

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("regulate_plus")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            metadata={
                "user_id": str(request.user.id),
                "username": request.user.username,
                "email": request.user.email,
            },
            subscription_data={
                "metadata": {
                    "user_id": str(request.user.id),
                    "username": request.user.username,
                    "email": request.user.email,
                },
            },
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(
                reverse("checkout_success")
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("checkout_cancelled")),
        )
        return redirect(session.url)

    except Exception:
        logger.exception("Stripe Checkout Error (subscribe)")
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("regulate_plus")


@login_required
def billing_details(request):
    sub = Subscription.objects.filter(user=request.user).first()
    stripe_customer_id = getattr(sub, "stripe_customer_id", None)

    if not stripe_customer_id:
        messages.error(
            request,
            "We couldn’t find your billing details yet. Try refreshing and clicking again.",
        )
        return redirect("regulate_plus")

    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url=request.build_absolute_uri(reverse("regulate_plus")),
        )
        return redirect(portal_session.url)

    except Exception:
        logger.exception("Stripe Portal Error")
        messages.error(request, "Couldn’t open billing page right now.")
        return redirect("regulate_plus")


@login_required
@require_GET
def checkout_success(request):
    """
    Stripe redirects here after Checkout.
    Webhooks are the source of truth, but we also attempt a best-effort sync for UX.
    """
    session_id = request.GET.get("session_id")

    if not session_id:
        _checkout_delayed_message(request)
        return redirect("regulate_plus")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        sub_id = session.get("subscription")
        cust_id = session.get("customer")

        if sub_id:
            stripe_sub = stripe.Subscription.retrieve(
                sub_id, expand=["latest_invoice", "customer", "items.data.price"]
            )
            updated = _upsert_subscription(request.user, stripe_sub, stripe_customer_id=cust_id)

            # If active but current_period_end missing, derive it for immediate display
            if updated.status == "active" and not updated.current_period_end:
                derived = _derive_period_end_from_anchor(stripe_sub)
                if derived:
                    updated.current_period_end = derived
                    updated.save(update_fields=["current_period_end"])

            messages.success(request, "Thanks — your plan is now active.")
        else:
            _checkout_delayed_message(request)

    except Exception:
        logger.warning("Stripe sync on success failed", exc_info=True)
        _checkout_delayed_message(request)

    return redirect("regulate_plus")


@login_required
@require_GET
def checkout_cancelled(request):
    messages.info(request, "Checkout cancelled — no changes were made.")
    return render(request, "billing/checkout_cancelled.html")
