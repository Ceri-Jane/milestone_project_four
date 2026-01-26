from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    # Admin logout → send back to admin login screen
    path(
        "admin/logout/",
        auth_views.LogoutView.as_view(
            next_page=settings.ADMIN_LOGOUT_REDIRECT_URL
        ),
        name="admin_logout",
    ),

    # Standard admin URLs
    path("admin/", admin.site.urls),

    # Core app routes (home, entries, dashboard, etc.)
    path("", include("core.urls")),

    # Accounts/profile routes
    path("account/", include("accounts.urls")),

    # Allauth (login, signup, reset, etc.)
    path("accounts/", include("allauth.urls")),

    # Billing / subscriptions
    path("billing/", include("billing.urls")),
]
