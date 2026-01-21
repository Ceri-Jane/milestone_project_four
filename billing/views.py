from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def _iso_or_none(dt):
    return dt.isoformat() if dt else None


@login_required
def start_trial(request):
    """
    Starts a 5-day free trial via Stripe Checkout.

    Notes:
    - If the user is already trialing/active, we send them back to dashboard.
    - If they've already used their trial before, we block it (1 trial per user).
    - We redirect straight to Stripe (no JSON), so it works even if JS doesn't load.
    """
    sub = getattr(request.user, "subscription", None)

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("dashboard")

    if sub and getattr(sub, "has_had_trial", False):
        messages.info(request, "You can only use the free trial once per user.")
        return redirect("dashboard")

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

        # Send user straight to Stripe Checkout
        return redirect(session.url)

    except Exception as e:
        print("Stripe Checkout Error (trial):", e)
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("dashboard")


@login_required
def start_subscription(request):
    """
    Paid subscription checkout (no trial).
    Used when trial has already been used (or for returning users).
    """
    sub = getattr(request.user, "subscription", None)

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("dashboard")

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

        return redirect(session.url)

    except Exception as e:
        print("Stripe Checkout Error (subscribe):", e)
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("dashboard")


@login_required
def billing_details(request):
    """
    Sends the user to Stripe Customer Portal to manage billing.

    Notes:
    - We need a stored stripe_customer_id on the user's Subscription row.
    - Return URL points back to the dashboard.
    """
    sub = getattr(request.user, "subscription", None)
    stripe_customer_id = getattr(sub, "stripe_customer_id", None)

    if not stripe_customer_id:
        messages.error(
            request,
            "We couldn’t find your billing details yet. Try refreshing and clicking again.",
        )
        return redirect("dashboard")

    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url=request.build_absolute_uri(reverse("dashboard")),
        )
        return redirect(portal_session.url)

    except Exception as e:
        print("Stripe Portal Error:", e)
        messages.error(request, "Couldn’t open billing page right now.")
        return redirect("dashboard")


@login_required
def trial_success(request):
    return render(request, "billing/trial_success.html")


@login_required
def trial_cancelled(request):
    return render(request, "billing/trial_cancelled.html")
