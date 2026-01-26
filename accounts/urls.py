from django.urls import path
from . import views

# Profile and account management routes
urlpatterns = [
    # View and manage user profile
    path("profile/", views.profile, name="profile"),

    # Update account username
    path("change-username/", views.change_username, name="change_username"),

    # Update account email
    path("change-email/", views.change_email, name="change_email"),
]
