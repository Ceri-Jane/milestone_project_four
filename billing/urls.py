from django.urls import path
from . import views


urlpatterns = [
    path("start-trial/", views.start_trial, name="start_trial"),
    path("trial-success/", views.trial_success, name="trial_success"),
    path("trial-cancelled/", views.trial_cancelled, name="trial_cancelled"),
]
