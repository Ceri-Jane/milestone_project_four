from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

# Hide unused allauth models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken


# -----------------------------
# HIDE ALLAUTH MODELS
# -----------------------------
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)


# -----------------------------
# USER ADMIN
# -----------------------------

@admin.display(description="Groups")
def group_list(obj):
    return ", ".join(g.name for g in obj.groups.all()) or "—"


@admin.display(description="Entries")
def entries_count(obj):
    return getattr(obj, "_entry_count", 0)


class CustomUserAdmin(UserAdmin):
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

    list_display = (
        "username",
        "email",
        entries_count,
        "is_active",
        "is_staff",
        "is_superuser",
        group_list,
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    search_fields = ("username", "email")
    ordering = ("username",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_entry_count=Count("entries", distinct=True)).prefetch_related("groups")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN
# -----------------------------

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count")

    @admin.display(description="Members")
    def member_count(self, obj):
        return User.objects.filter(groups=obj).count()


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
