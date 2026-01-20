from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .models import Subscription


stripe.api_key = settings.STRIPE_SECRET_KEY


def _to_dt(ts):
    """Convert Stripe unix timestamp -> aware datetime (UTC)."""
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


def _upsert_subscription(user, stripe_sub):
    """
    Create or update our local Subscription record from a Stripe subscription object.
    NOTE: This uses hasattr checks so it won't crash if your model fields differ.
    """
    sub_id = stripe_sub.get("id")
    cust_id = stripe_sub.get("customer")
    status = stripe_sub.get("status")

    current_period_end = _to_dt(stripe_sub.get("current_period_end"))
    trial_end = _to_dt(stripe_sub.get("trial_end"))
    cancel_at_period_end = stripe_sub.get("cancel_at_period_end", False)

    obj, _created = Subscription.objects.get_or_create(user=user)

    if hasattr(obj, "stripe_subscription_id"):
        obj.stripe_subscription_id = sub_id
    if hasattr(obj, "stripe_customer_id"):
        obj.stripe_customer_id = cust_id
    if hasattr(obj, "status"):
        obj.status = status
    if hasattr(obj, "current_period_end"):
        obj.current_period_end = current_period_end
    if hasattr(obj, "trial_end"):
        obj.trial_end = trial_end
    if hasattr(obj, "cancel_at_period_end"):
        obj.cancel_at_period_end = cancel_at_period_end

    obj.save()
    return obj


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook endpoint:
    - Verifies signature using STRIPE_WEBHOOK_SECRET
    - Handles key events to keep Subscription table in sync
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse("Missing STRIPE_WEBHOOK_SECRET", status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    event_type = event["type"]
    data_object = event["data"]["object"]

    # Subscription created/updated
    if event_type in ("customer.subscription.created", "customer.subscription.updated"):
        metadata = data_object.get("metadata", {})
        user_id = metadata.get("user_id")

        if user_id:
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                _upsert_subscription(user, data_object)
            except User.DoesNotExist:
                pass

    # Subscription deleted/canceled
    elif event_type == "customer.subscription.deleted":
        sub_id = data_object.get("id")
        try:
            local = Subscription.objects.get(stripe_subscription_id=sub_id)
            if hasattr(local, "status"):
                local.status = "canceled"
                local.save()
        except Subscription.DoesNotExist:
            pass

    # Checkout completed (helpful when the hosted checkout succeeds)
    elif event_type == "checkout.session.completed":
        subscription_id = data_object.get("subscription")
        if subscription_id:
            try:
                stripe_sub = stripe.Subscription.retrieve(subscription_id)
                metadata = stripe_sub.get("metadata", {})
                user_id = metadata.get("user_id")

                if user_id:
                    User = get_user_model()
                    user = User.objects.get(id=user_id)
                    _upsert_subscription(user, stripe_sub)
            except Exception:
                pass

    return HttpResponse(status=200)
