from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

    elif event_type == "customer.subscription.deleted":
        sub_id = data_object.get("id")
        try:
            local = Subscription.objects.get(stripe_subscription_id=sub_id)
            local.status = "canceled"
            local.save()
        except Subscription.DoesNotExist:
            pass

    elif event_type == "checkout.session.completed":
        # Checkout session object
        subscription_id = data_object.get("subscription")
        customer_id = data_object.get("customer")

        # Prefer session metadata, fall back to subscription metadata
        user_id = None
        session_meta = data_object.get("metadata", {})
        if session_meta:
            user_id = session_meta.get("user_id")

        if subscription_id:
            try:
                stripe_sub = stripe.Subscription.retrieve(subscription_id)
                if not user_id:
                    sub_meta = stripe_sub.get("metadata", {})
                    user_id = sub_meta.get("user_id")

                if user_id:
                    User = get_user_model()
                    user = User.objects.get(id=user_id)
                    _upsert_subscription(user, stripe_sub, stripe_customer_id=customer_id)
            except Exception:
                pass

    return HttpResponse(status=200)
