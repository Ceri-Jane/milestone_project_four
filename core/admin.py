from django.contrib import admin
from django.contrib.sites.models import Site

from .models import (
    EmotionWord,
    Entry,
    EntryRevision,
    SiteAnnouncement,
    SupportTicket,
)


@admin.register(EmotionWord)
class EmotionWordAdmin(admin.ModelAdmin):
    list_display = ("word",)
    search_fields = ("word",)
    ordering = ("word",)


@admin.register(SiteAnnouncement)
class SiteAnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "live_status",
        "starts_at",
        "ends_at",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "message")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")

    def live_status(self, obj):
        return obj.is_live

    live_status.boolean = True
    live_status.short_description = "Live"

    fieldsets = (
        (None, {"fields": ("title", "message", "is_active")}),
        ("Schedule (optional)", {"fields": ("starts_at", "ends_at")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "subject", "user", "email")
    list_filter = ("status", "created_at")
    search_fields = ("subject", "message", "user__username", "user__email", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("status",)}),
        ("Who", {"fields": ("user", "email")}),
        ("Message", {"fields": ("subject", "message")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


# Lock down private user content in admin
for model in (Entry, EntryRevision):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
