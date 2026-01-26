from django.apps import AppConfig


# App configuration for billing and subscriptions
class BillingConfig(AppConfig):
    # Default primary key field type
    default_auto_field = 'django.db.models.BigAutoField'

    # Application label
    name = 'billing'
