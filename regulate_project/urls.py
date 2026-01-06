from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from core import views as core_views

urlpatterns = [
    # Admin logout → send back to admin login screen
    path(
        "admin/logout/",
        auth_views.LogoutView.as_view(
            next_page=settings.ADMIN_LOGOUT_REDIRECT_URL
        ),
        name="admin_logout",
    ),

    # Standard admin URLs (now using the custom logout above)
    path("admin/", admin.site.urls),

    # Home / dashboard
    path("", core_views.home, name="home"),

    # Core app routes (new entry, lists, etc)
    path("", include("core.urls")),  # include all core routes

    # Custom account views (profile etc.)
    path("account/", include("accounts.urls")),

    # Account system (login, signup, reset, etc) via allauth
    path("accounts/", include("allauth.urls")),
]