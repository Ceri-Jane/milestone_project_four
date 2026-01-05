# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from core.models import Entry

# Hide Allauth admin panels we do not need
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken


# -----------------------------
# REMOVE EMAIL + SOCIAL MODELS
# -----------------------------
# These still exist — just hidden them from admin UI
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)


# -----------------------------
# USER ADMIN CUSTOMISATIONS
# -----------------------------

def group_list(obj):
    return ", ".join(g.name for g in obj.groups.all()) or "—"
group_list.short_description = "Groups"


def total_entries(obj):
    """
    Number of Regulate entries for this user,
    clickable to filtered Entry list.
    """
    count = Entry.objects.filter(user=obj).count()

    url = (
        reverse("admin:core_entry_changelist")
        + "?"
        + urlencode({"user__id__exact": obj.id})
    )

    return format_html('<a href="{}">{}</a>', url, count)

total_entries.short_description = "Entries"


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        group_list,
        total_entries,
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )


# Replace default User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN CUSTOMISATIONS
# -----------------------------

class CustomGroupAdmin(admin.ModelAdmin):

    list_display = ("name", "member_count")

    def member_count(self, obj):
        UserModel = admin.site._registry[User].model
        return UserModel.objects.filter(groups=obj).count()

    member_count.short_description = "Members"


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
