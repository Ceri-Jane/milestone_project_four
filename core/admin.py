from django.contrib import admin, messages
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

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
    list_display = ("created_at", "status", "subject", "user", "email", "mark_replied_button")
    list_filter = ("status", "created_at")
    search_fields = ("subject", "message", "user__username", "user__email", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    actions = ("mark_as_replied",)

    fieldsets = (
        (None, {"fields": ("status",)}),
        ("Who", {"fields": ("user", "email")}),
        ("Message", {"fields": ("subject", "message")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )

    # ---------- helpers ----------

    def _get_replied_status_value(self):
        """
        Pick the best 'replied/resolved/closed' status from the model field choices.
        This keeps admin robust even if you rename statuses later.
        """
        field = SupportTicket._meta.get_field("status")
        choices = [c[0] for c in (field.choices or []) if c and c[0] is not None]

        if not choices:
            return None

        preferred = ("replied", "resolved", "closed", "done")
        for val in preferred:
            if val in choices:
                return val

        # Fallback: last choice (often 'closed'/'resolved' in many enums)
        return choices[-1]

    def _set_replied(self, queryset):
        target = self._get_replied_status_value()
        if not target:
            return 0
        return queryset.exclude(status=target).update(status=target)

    # ---------- list page button ----------

    @admin.display(description="Reply handled")
    def mark_replied_button(self, obj):
        target = self._get_replied_status_value()

        # If we can't detect a valid target status, don't render a misleading button
        if not target:
            return "—"

        # If already in target status, show a non-clickable label
        if obj.status == target:
            return format_html(
                '<span style="display:inline-block;padding:6px 10px;border-radius:999px;'
                'background:#e7f6ee;border:1px solid #a2d9c9;color:#2a5e4f;font-weight:600;">'
                'Replied</span>'
            )

        url = reverse("admin:core_supportticket_mark_replied", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="padding:6px 10px;">Mark replied</a>',
            url,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:ticket_id>/mark-replied/",
                self.admin_site.admin_view(self.mark_replied_view),
                name="core_supportticket_mark_replied",
            ),
        ]
        return custom_urls + urls

    def mark_replied_view(self, request, ticket_id):
        target = self._get_replied_status_value()
        if not target:
            self.message_user(
                request,
                "Couldn’t mark as replied because no status choices were detected.",
                level=messages.ERROR,
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", ".."))

        try:
            ticket = SupportTicket.objects.get(pk=ticket_id)
        except SupportTicket.DoesNotExist:
            self.message_user(request, "Support ticket not found.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", ".."))

        if ticket.status != target:
            ticket.status = target
            ticket.save(update_fields=["status"])
            self.message_user(request, "Ticket marked as replied.", level=messages.SUCCESS)
        else:
            self.message_user(request, "Ticket is already marked as replied.", level=messages.INFO)

        changelist_url = reverse("admin:core_supportticket_changelist")
        return HttpResponseRedirect(changelist_url)

    # ---------- bulk action ----------

    @admin.action(description="Mark selected tickets as replied")
    def mark_as_replied(self, request, queryset):
        updated = self._set_replied(queryset)
        if updated:
            self.message_user(request, f"{updated} ticket(s) marked as replied.", level=messages.SUCCESS)
        else:
            self.message_user(request, "No tickets were updated.", level=messages.INFO)


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
