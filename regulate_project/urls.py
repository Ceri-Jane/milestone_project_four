from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
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
