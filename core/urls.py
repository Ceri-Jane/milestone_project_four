from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Static pages
    path("faq/", views.faq, name="faq"),
    path("support/", views.support, name="support"),  # crisis/support info page
    path("contact/", views.contact, name="contact"),  # NEW: non-urgent inbox form

    # Create new entry
    path("new-entry/", views.new_entry, name="new_entry"),

    # Dashboard (hub page)
    path("dashboard/", views.dashboard, name="dashboard"),

    # My Entries – dedicated route for list/search view
    path("entries/", views.my_entries, name="my_entries"),

    # View single entry
    path("entry/<int:entry_id>/", views.view_entry, name="view_entry"),

    # Edit entry
    path("entry/<int:entry_id>/edit/", views.edit_entry, name="edit_entry"),

    # Delete entry
    path("entry/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),

    # API
    path("api/supportive-phrase/", views.supportive_phrase, name="supportive_phrase"),
]
