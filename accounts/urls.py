from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("change-username/", views.change_username, name="change_username"),
    path("change-email/", views.change_email, name="change_email"),
]
