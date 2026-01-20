from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def _iso_or_none(dt):
    return dt.isoformat() if dt else None


@login_required
def start_trial(request):
    """
    Start a 5-day free trial (ONLY if user has never had one).
    Returns JSON for JS to redirect or show a friendly message.
    """
    sub = getattr(request.user, "subscription", None)

    # Block if already active or currently trialing
    if sub and sub.status in ["trialing", "active"]:
        return JsonResponse(
            {
                "ok": False,
                "reason": "already_subscribed",
                "status": sub.status,
                "trial_end": _iso_or_none(sub.trial_end),
            },
            status=409,
        )

    # Block if they've EVER had a trial before
    if sub and getattr(sub, "has_had_trial", False):
        return JsonResponse(
            {
                "ok": False,
                "reason": "trial_already_used",
                "status": sub.status,
            },
            status=409,
        )

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            subscription_data={
                "trial_period_days": 5,
                "metadata": {
                    "user_id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                },
            },
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(reverse("trial_success")),
            cancel_url=request.build_absolute_uri(reverse("trial_cancelled")),
        )

        return JsonResponse({"ok": True, "session_url": session.url})

    except Exception as e:
        print("Stripe Checkout Error (trial):", e)
        return JsonResponse(
            {"ok": False, "reason": "stripe_error"},
            status=500,
        )


@login_required
def start_subscription(request):
    """
    Paid subscription checkout (NO trial).
    Use this for users who already used their trial and cancelled,
    or anyone returning later.
    """
    sub = getattr(request.user, "subscription", None)

    if sub and sub.status in ["trialing", "active"]:
        return JsonResponse(
            {
                "ok": False,
                "reason": "already_subscribed",
                "status": sub.status,
                "trial_end": _iso_or_none(sub.trial_end),
            },
            status=409,
        )

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            subscription_data={
                "metadata": {
                    "user_id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                },
            },
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(reverse("trial_success")),
            cancel_url=request.build_absolute_uri(reverse("trial_cancelled")),
        )

        return JsonResponse({"ok": True, "session_url": session.url})

    except Exception as e:
        print("Stripe Checkout Error (subscribe):", e)
        return JsonResponse(
            {"ok": False, "reason": "stripe_error"},
            status=500,
        )


@login_required
def billing_details(request):
    """
    Simple "Billing details" page placeholder for now.
    Later we'll replace/extend this with Stripe Customer Portal.
    """
    sub = getattr(request.user, "subscription", None)
    return render(request, "billing/billing_details.html", {"subscription": sub})


@login_required
def trial_success(request):
    return render(request, "billing/trial_success.html")


@login_required
def trial_cancelled(request):
    return render(request, "billing/trial_cancelled.html")
