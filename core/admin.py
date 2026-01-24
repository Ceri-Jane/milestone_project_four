from django.contrib import admin
from django.contrib.sites.models import Site

from .models import EmotionWord, Entry, EntryRevision


@admin.register(EmotionWord)
class EmotionWordAdmin(admin.ModelAdmin):
    """Simple searchable list of emotion words."""
    list_display = ("word",)
    search_fields = ("word",)
    ordering = ("word",)


# --------------------------------------------------
# LOCK DOWN PRIVATE USER CONTENT IN ADMIN
# --------------------------------------------------
# Unregister Entry + EntryRevision so staff/admin can't browse them in /admin/
for model in (Entry, EntryRevision):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


# --------------------------------------------------
# HIDE "Sites" PANEL FROM ADMIN (keeps framework)
# --------------------------------------------------
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
