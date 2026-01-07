from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

import stripe

from .models import Subscription


# Use secret key from environment
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def start_trial(request):
    """
    Create a Stripe Checkout Session for starting a Regulate+ subscription.

    Behaviour:
    - If user already has an active or trial subscription → block duplicate signup
    - Otherwise creates a hosted Stripe Checkout session
    - Trial period is applied by Stripe (from the Price settings)
    """

    subscription = getattr(request.user, "subscription", None)

    if subscription and subscription.status in ["trialing", "active"]:
        messages.info(request, "You already have an active Regulate+ plan.")
        return redirect("dashboard")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[
                {
                    "price": settings.STRIPE_PRICE_ID,
                    "quantity": 1,
                }
            ],
            subscription_data={
                # Trial is configured in Stripe Price
                "metadata": {
                    "user_id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                }
            },
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(
                reverse("trial_success")
            ),
            cancel_url=request.build_absolute_uri(
                reverse("trial_cancelled")
            ),
        )

        # Return JSON if called via JS button
        return JsonResponse({"session_url": session.url})

    except Exception as e:
        print("Stripe Checkout Error:", e)

        messages.error(
            request,
            "Sorry — something went wrong starting your free trial."
        )
        return redirect("dashboard")


@login_required
def trial_success(request):
    """
    Temporary placeholder page after checkout success.
    A webhook will later confirm subscription + create DB record.
    """
    return render(request, "billing/trial_success.html")


@login_required
def trial_cancelled(request):
    """
    Page shown when the user exits Stripe Checkout without completing signup.
    """
    return render(request, "billing/trial_cancelled.html")
