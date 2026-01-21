from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

import stripe

from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def start_trial(request):
    """
    Starts a 5-day free trial via Stripe Checkout.

    Fixes:
    - SAFE subscription lookup (no getattr OneToOne crash)
    - Creates/updates a local Subscription row immediately so trial can't be started repeatedly
      even if webhook is delayed/misconfigured.
    """
    sub = Subscription.objects.filter(user=request.user).first()

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("dashboard")

    # If they've ever used a trial, block it
    if sub and sub.has_had_trial:
        messages.info(request, "You can only use the free trial once per user.")
        return redirect("dashboard")

    # Ensure a local row exists BEFORE sending them to Stripe
    # This prevents repeated trial checkouts if webhook hasn't updated yet.
    if not sub:
        sub = Subscription.objects.create(
            user=request.user,
            status="incomplete",
            has_had_trial=True,
        )
    else:
        # Mark trial as used as soon as they start the checkout flow
        sub.has_had_trial = True
        # Keep a neutral status until webhook confirms trialing/active
        if sub.status not in ["trialing", "active"]:
            sub.status = "incomplete"
        sub.save(update_fields=["has_had_trial", "status", "updated_at"])

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

        return redirect(session.url)

    except Exception as e:
        print("Stripe Checkout Error (trial):", e)
        messages.error(
            request,
            "Sorry — we couldn’t open Stripe Checkout. Please try again."
        )
        return redirect("dashboard")


@login_required
def start_subscription(request):
    """
    Paid subscription checkout (no trial).
    """
    sub = Subscription.objects.filter(user=request.user).first()

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
        messages.error(
            request,
            "Sorry — we couldn’t open Stripe Checkout. Please try again."
        )
        return redirect("dashboard")


@login_required
def billing_details(request):
    """
    Sends the user to Stripe Customer Portal to manage billing.
    """
    sub = Subscription.objects.filter(user=request.user).first()
    stripe_customer_id = sub.stripe_customer_id if sub else None

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
