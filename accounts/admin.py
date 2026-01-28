from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

User = get_user_model()


# -----------------------------
# HIDE UNUSED ALLAUTH MODELS
# -----------------------------
for model in (EmailAddress, SocialAccount, SocialApp, SocialToken):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


# -----------------------------
# USER ADMIN
# -----------------------------

class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "entries_count",
        "is_active",
        "is_staff",
        "is_superuser",
        "group_list",
    )

    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Contact", {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _entry_count=Count("entries", distinct=True)
        ).prefetch_related("groups")

    def entries_count(self, obj):
        return getattr(obj, "_entry_count", 0)

    entries_count.short_description = "Entries"

    def group_list(self, obj):
        return ", ".join(obj.groups.values_list("name", flat=True)) or "—"

    group_list.short_description = "Groups"


# Replace default User admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN
# -----------------------------

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count")

    def member_count(self, obj):
        return User.objects.filter(groups=obj).count()

    member_count.short_description = "Members"


try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

admin.site.register(Group, CustomGroupAdmin)
