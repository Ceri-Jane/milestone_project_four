from django.apps import AppConfig


# Core application configuration
class CoreConfig(AppConfig):
    # Default primary key field type
    default_auto_field = "django.db.models.BigAutoField"

    # Application label
    name = "core"
