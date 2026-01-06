from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # homepage / landing

    # Create new entry
    path("new-entry/", views.new_entry, name="new_entry"),

    # Dashboard (hub page)
    path("dashboard/", views.dashboard, name="dashboard"),

    # My Entries – dedicated route for list/search view
    path("entries/", views.my_entries, name="my_entries"),

    # ----- ENTRY ACTION ROUTES -----

    # View single entry
    path("entry/<int:entry_id>/", views.view_entry, name="view_entry"),

    # Edit entry
    path("entry/<int:entry_id>/edit/", views.edit_entry, name="edit_entry"),

    # Delete entry
    path("entry/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),

    # ----- API ROUTES -----

    # Supportive phrase / quotes (EXTERNAL API integration)
    path(
        "api/supportive-phrase/",
        views.supportive_phrase,
        name="supportive_phrase",
    ),
]
