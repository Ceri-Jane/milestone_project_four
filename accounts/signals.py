# accounts/signals.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver


User = get_user_model()


@receiver(post_migrate)
def create_site_user_group(sender, **kwargs):
    """
    Make sure the 'Site User' group always exists
    after migrations (both locally and on Heroku).
    """
    Group.objects.get_or_create(name="Site User")


@receiver(post_save, sender=User)
def add_user_to_site_user_group(sender, instance, created, **kwargs):
    """
    Whenever a new user is created (signup or via admin),
    automatically add them to the 'Site User' group.
    """
    if not created:
        return

    group, _ = Group.objects.get_or_create(name="Site User")
    instance.groups.add(group)
