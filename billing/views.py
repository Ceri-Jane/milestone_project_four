from datetime import datetime, timezone as dt_timezone
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import Subscription

# Stripe API configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


def _to_dt(ts):
    """Convert Stripe timestamps to timezone-aware datetimes."""
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


def _upsert_subscription(user, stripe_sub, stripe_customer_id=None):
    """Create/update a user's Subscription record from Stripe subscription data."""
    sub_id = stripe_sub.get("id")
    cust_id = stripe_customer_id or stripe_sub.get("customer")
    status = stripe_sub.get("status")

    current_period_end = _to_dt(stripe_sub.get("current_period_end"))
    trial_end = _to_dt(stripe_sub.get("trial_end"))

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
    """
    Consistent message for the common webhook-delay case (assessor-friendly).
    """
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

    # Best-effort sync: if user is active but period dates are missing, fetch once from Stripe
    if sub and status == "active" and not getattr(sub, "current_period_end", None):
        stripe_sub_id = getattr(sub, "stripe_subscription_id", None)
        if stripe_sub_id:
            try:
                stripe_sub = stripe.Subscription.retrieve(stripe_sub_id)
                sub = _upsert_subscription(request.user, stripe_sub)
                status = getattr(sub, "status", status)
            except Exception:
                logger.warning("Stripe sync on Regulate+ page failed", exc_info=True)

    trial_end = getattr(sub, "trial_end", None)
    period_end = getattr(sub, "current_period_end", None)

    trial_days_left = None
    if status == "trialing" and trial_end:
        today = timezone.now().date()
        end_date = trial_end.date()
        trial_days_left = (end_date - today).days
        if trial_days_left < 0:
            trial_days_left = 0

    context = {
        "subscription": sub,
        "subscription_status": status,
        "is_active_plan": status in ["trialing", "active"],
        "has_had_trial": getattr(sub, "has_had_trial", False),
        "trial_end": trial_end,
        "trial_days_left": trial_days_left,
        "current_period_end": period_end,
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
            stripe_sub = stripe.Subscription.retrieve(sub_id)
            _upsert_subscription(request.user, stripe_sub, stripe_customer_id=cust_id)
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
