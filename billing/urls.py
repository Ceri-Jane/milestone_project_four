from django.urls import path
from . import views
from . import webhooks

# Billing and subscription routes
urlpatterns = [
    # Start free trial checkout
    path("start-trial/", views.start_trial, name="start_trial"),

    # Start paid subscription checkout
    path("start-subscription/", views.start_subscription, name="start_subscription"),

    # Trial flow callbacks
    path("trial-success/", views.trial_success, name="trial_success"),
    path("trial-cancelled/", views.trial_cancelled, name="trial_cancelled"),

    # Stripe billing portal
    path("manage/", views.billing_details, name="billing_details"),

    # Stripe webhook endpoint
    path("webhook/", webhooks.stripe_webhook, name="stripe_webhook"),
]
