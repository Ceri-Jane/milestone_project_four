from django.contrib import admin
from .models import Entry  # register Entry model


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Basic admin view for entries."""
    list_display = ("user", "mood", "created_at")  # quick overview
    list_filter = ("mood", "created_at")  # easy filtering
    search_fields = ("notes", "emotion_words")  # search text fields
