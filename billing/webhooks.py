# billing/webhooks.py

from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


def _to_dt(ts):
    """Convert Stripe unix timestamps to timezone-aware UTC datetimes."""
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


def _upsert_subscription(user, stripe_sub):
    """
    Create/update the local Subscription record from a Stripe subscription payload.
    """
    sub_id = stripe_sub.get("id")
    cust_id = stripe_sub.get("customer")
    status = stripe_sub.get("status")

    current_period_end = _to_dt(stripe_sub.get("current_period_end"))
    trial_end = _to_dt(stripe_sub.get("trial_end"))
    cancel_at_period_end = stripe_sub.get("cancel_at_period_end", False)

    # Handy while testing locally / reading Heroku logs
    print("UPSERT:", status, "cancel_at_period_end=", cancel_at_period_end)

    obj, _created = Subscription.objects.get_or_create(user=user)

    obj.stripe_subscription_id = sub_id
    obj.stripe_customer_id = cust_id
    obj.status = status
    obj.current_period_end = current_period_end
    obj.trial_end = trial_end
    obj.cancel_at_period_end = bool(cancel_at_period_end)

    # Trial is only allowed once, so flag it as soon as we've seen a trial end timestamp.
    if trial_end:
        obj.has_had_trial = True

    obj.save()
    return obj


def _get_user_from_subscription_or_session(sub_obj=None, session_obj=None):
    """
    Try to find the user_id from:
    - subscription.metadata.user_id
    - session.subscription_data.metadata.user_id
    - session.metadata.user_id
    """
    user_id = None

    if sub_obj:
        user_id = (sub_obj.get("metadata") or {}).get("user_id")

    if not user_id and session_obj:
        sub_data = session_obj.get("subscription_data") or {}
        user_id = (sub_data.get("metadata") or {}).get("user_id")

    if not user_id and session_obj:
        user_id = (session_obj.get("metadata") or {}).get("user_id")

    if not user_id:
        return None

    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def _get_local_subscription_from_ids(sub_obj):
    """
    Find a local Subscription using Stripe IDs.
    This is important because portal-driven events don't reliably include metadata.user_id.
    """
    sub_id = sub_obj.get("id")
    customer_id = sub_obj.get("customer")

    local = None
    if sub_id:
        local = (
            Subscription.objects.filter(stripe_subscription_id=sub_id)
            .select_related("user")
            .first()
        )

    if not local and customer_id:
        local = (
            Subscription.objects.filter(stripe_customer_id=customer_id)
            .select_related("user")
            .first()
        )

    return local


@csrf_exempt
def stripe_webhook(request):
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

    print("STRIPE EVENT:", event_type)

    if event_type in ("customer.subscription.created", "customer.subscription.updated"):
        # 1) First try to match by Stripe IDs (most reliable for portal updates/cancellations)
        local = _get_local_subscription_from_ids(data_object)
        if local and getattr(local, "user", None):
            _upsert_subscription(local.user, data_object)
        else:
            # 2) Fallback to metadata mapping (useful during initial checkout flow)
            user = _get_user_from_subscription_or_session(sub_obj=data_object)
            if user:
                _upsert_subscription(user, data_object)

    elif event_type == "customer.subscription.deleted":
        # Subscription fully ended on Stripe side (not just cancel_at_period_end)
        local = _get_local_subscription_from_ids(data_object)
        if local:
            local.status = "canceled"
            local.cancel_at_period_end = False
            local.save()

    elif event_type == "checkout.session.completed":
        subscription_id = data_object.get("subscription")
        customer_id = data_object.get("customer")

        if subscription_id:
            try:
                stripe_sub = stripe.Subscription.retrieve(subscription_id)

                user = _get_user_from_subscription_or_session(
                    sub_obj=stripe_sub,
                    session_obj=data_object,
                )

                if user:
                    obj = _upsert_subscription(user, stripe_sub)

                    # Belt and braces: ensure we store the customer id if we didn't already.
                    if customer_id and not obj.stripe_customer_id:
                        obj.stripe_customer_id = customer_id
                        obj.save()
            except Exception as e:
                print("checkout.session.completed handler error:", e)

    return HttpResponse(status=200)
