from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


def _to_dt(ts):
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


def _upsert_subscription(user, stripe_sub, stripe_customer_id=None):
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

    if trial_end or status == "trialing":
        obj.has_had_trial = True

    obj.save()
    return obj


@login_required
def start_trial(request):
    sub = Subscription.objects.filter(user=request.user).first()

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("dashboard")

    if sub and sub.has_had_trial:
        messages.info(request, "You can only use the free trial once per user.")
        return redirect("dashboard")

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
                reverse("trial_success")
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("trial_cancelled")),
        )
        return redirect(session.url)

    except Exception as e:
        print("Stripe Checkout Error (trial):", e)
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("dashboard")


@login_required
def start_subscription(request):
    sub = Subscription.objects.filter(user=request.user).first()

    if sub and sub.status in ["trialing", "active"]:
        messages.info(request, "You already have an active plan.")
        return redirect("dashboard")

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
                reverse("trial_success")
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("trial_cancelled")),
        )
        return redirect(session.url)

    except Exception as e:
        print("Stripe Checkout Error (subscribe):", e)
        messages.error(request, "Sorry — we couldn’t open Stripe Checkout. Please try again.")
        return redirect("dashboard")


@login_required
def billing_details(request):
    sub = Subscription.objects.filter(user=request.user).first()
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
            return_url=request.build_absolute_uri(reverse("profile")),
        )
        return redirect(portal_session.url)

    except Exception as e:
        print("Stripe Portal Error:", e)
        messages.error(request, "Couldn’t open billing page right now.")
        return redirect("dashboard")


@login_required
def trial_success(request):
    session_id = request.GET.get("session_id")

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            sub_id = session.get("subscription")
            cust_id = session.get("customer")

            if sub_id:
                stripe_sub = stripe.Subscription.retrieve(sub_id)
                _upsert_subscription(request.user, stripe_sub, stripe_customer_id=cust_id)

        except Exception as e:
            print("Stripe sync on success failed:", e)

    return render(request, "billing/trial_success.html")


@login_required
def trial_cancelled(request):
    return render(request, "billing/trial_cancelled.html")
