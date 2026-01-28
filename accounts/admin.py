from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

User = get_user_model()


# -----------------------------
# ADMIN BRANDING
# -----------------------------
admin.site.site_header = "Regulate Admin"
admin.site.site_title = "Regulate Admin"
admin.site.index_title = "Administration"


# -----------------------------
# HIDE UNUSED ALLAUTH MODELS
# -----------------------------
for model in (EmailAddress, SocialAccount, SocialApp, SocialToken):
    if model in admin.site._registry:
        admin.site.unregister(model)


# -----------------------------
# OPTIONAL BILLING INLINE
# -----------------------------
try:
    from billing.admin import SubscriptionInline
except Exception:
    SubscriptionInline = None


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
                )
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


if SubscriptionInline:
    CustomUserAdmin.inlines = [SubscriptionInline]


# Replace default User admin
if User in admin.site._registry:
    admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------
# GROUP ADMIN
# -----------------------------
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count")

    def member_count(self, obj):
        return User.objects.filter(groups=obj).count()

    member_count.short_description = "Members"


if Group in admin.site._registry:
    admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
