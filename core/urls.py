from django.urls import path
from . import views

urlpatterns = [
    path("new-entry/", views.new_entry, name="new_entry"),  # new entry page
]
