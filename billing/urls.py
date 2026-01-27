from django.urls import path
from . import views
from . import webhooks

# Billing and subscription routes
urlpatterns = [
    # Regulate+ hub (trial / upgrade / manage billing)
    path("regulate-plus/", views.regulate_plus, name="regulate_plus"),

    # Start free trial checkout
    path("start-trial/", views.start_trial, name="start_trial"),

    # Start paid subscription checkout
    path("start-subscription/", views.start_subscription, name="start_subscription"),

    # Checkout flow callbacks (trial + paid)
    path("checkout-success/", views.checkout_success, name="checkout_success"),
    path("checkout-cancelled/", views.checkout_cancelled, name="checkout_cancelled"),

    # Stripe billing portal
    path("manage/", views.billing_details, name="billing_details"),

    # Stripe webhook endpoint (DO NOT TOUCH)
    path("webhook/", webhooks.stripe_webhook, name="stripe_webhook"),
]
