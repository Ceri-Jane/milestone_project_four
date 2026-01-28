from django.contrib import admin

from .models import Subscription


# -----------------------------
# SUBSCRIPTION ADMIN
# -----------------------------
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "has_had_trial",
        "created_at",
        "trial_end",
        "stripe_customer_id",
        "stripe_subscription_id",
    )
    list_filter = ("status", "has_had_trial")
    search_fields = (
        "user__username",
        "user__email",
        "stripe_customer_id",
        "stripe_subscription_id",
    )
    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "stripe_customer_id",
        "stripe_subscription_id",
        "has_had_trial",
        "status",
        "trial_end",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("user", "status", "has_had_trial")}),
        ("Dates", {"fields": ("trial_end",)}),
        ("Stripe", {"fields": ("stripe_customer_id", "stripe_subscription_id")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


# -----------------------------
# INLINE (USED BY ACCOUNTS ADMIN)
# -----------------------------
class SubscriptionInline(admin.StackedInline):
    model = Subscription
    can_delete = False
    extra = 0
    max_num = 1

    readonly_fields = (
        "stripe_customer_id",
        "stripe_subscription_id",
        "status",
        "has_had_trial",
        "trial_end",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("status", "has_had_trial")}),
        ("Dates", {"fields": ("trial_end",)}),
        ("Stripe", {"fields": ("stripe_customer_id", "stripe_subscription_id")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )
