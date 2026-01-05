from django.contrib import admin
from django.contrib.sites.models import Site

from .models import EmotionWord, Entry, EntryRevision


@admin.register(EmotionWord)
class EmotionWordAdmin(admin.ModelAdmin):
    """Simple searchable list of emotion words."""
    list_display = ("word",)
    search_fields = ("word",)
    ordering = ("word",)


class EntryRevisionInline(admin.TabularInline):
    """
    Read-only inline history for each Entry.
    Shows all past versions underneath the main entry.
    """
    model = EntryRevision
    extra = 0
    can_delete = False

    readonly_fields = (
        "created_at",
        "mood",
        "hue",
        "emotion_words",
        "notes",
    )

    fields = (
        "created_at",
        "mood",
        "hue",
        "emotion_words",
        "notes",
    )

    ordering = ("-created_at",)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """
    Main view for mood entries.
    Useful list view + tidy fieldsets and a revision history inline.
    """

    # ------- LIST VIEW -------
    list_display = (
        "user",
        "created_at",
        "mood",
        "hue",
        "short_emotions",
    )
    list_filter = ("mood", "created_at")
    search_fields = (
        "user__username",
        "emotion_words",
        "notes",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    # ------- FORM LAYOUT -------
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Who & When", {
            "fields": ("user", "created_at"),
        }),
        ("Mood & Colour", {
            "fields": ("mood", "hue"),
        }),
        ("Emotion Words", {
            "fields": ("emotion_words",),
        }),
        ("Notes", {
            "fields": ("notes",),
        }),
    )

    # Show revisions under each Entry
    inlines = [EntryRevisionInline]

    # ------- CUSTOM COLUMN -------
    def short_emotions(self, obj):
        """
        Short preview of the emotion words column.
        """
        if not obj.emotion_words:
            return "—"
        text = obj.emotion_words.strip()
        return text if len(text) <= 40 else text[:37] + "..."
    short_emotions.short_description = "Emotions"


@admin.register(EntryRevision)
class EntryRevisionAdmin(admin.ModelAdmin):
    """
    Separate read-only view for revisions.
    Mostly for debugging / auditing.
    """
    list_display = ("entry", "created_at", "mood")
    list_filter = ("mood", "created_at")
    search_fields = (
        "entry__user__username",
        "emotion_words",
        "notes",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    readonly_fields = (
        "entry",
        "created_at",
        "mood",
        "hue",
        "emotion_words",
        "notes",
    )


# --------------------------------------------------
# HIDE "Sites" PANEL FROM ADMIN (keeps framework)
# --------------------------------------------------
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
