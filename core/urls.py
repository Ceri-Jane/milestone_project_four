from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # homepage / landing
    path("new-entry/", views.new_entry, name="new_entry"),  # new entry page
    path("dashboard/", views.dashboard, name="dashboard"),  # dashboard page
]
