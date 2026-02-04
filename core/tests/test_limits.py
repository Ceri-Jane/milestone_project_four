from django.contrib.auth import get_user_model
from django.test import TestCase

from billing.models import Subscription
from core.limits import FREE_ENTRY_LIMIT, is_free_locked
from core.models import Entry


User = get_user_model()


class TestFreePlanLimits(TestCase):
    """Unit tests for free-plan gating logic in core/limits.py."""

    def setUp(self):
        self.password = "pass12345!"

    def _make_user(self, username):
        return User.objects.create_user(username=username, password=self.password)

    def _make_entries(self, user, count):
        """Create minimal valid entries for a user (mood is required)."""
        Entry.objects.bulk_create([Entry(user=user, mood=3, hue="50") for _ in range(count)])

    def test_free_user_below_limit_is_not_locked(self):
        user = self._make_user("u_below")
        self._make_entries(user, FREE_ENTRY_LIMIT - 1)

        self.assertFalse(is_free_locked(user))

    def test_free_user_at_limit_is_locked(self):
        user = self._make_user("u_at")
        self._make_entries(user, FREE_ENTRY_LIMIT)

        self.assertTrue(is_free_locked(user))

    def test_active_subscription_user_is_never_locked(self):
        user = self._make_user("u_active")
        Subscription.objects.create(user=user, status="active")
        self._make_entries(user, FREE_ENTRY_LIMIT + 25)

        self.assertFalse(is_free_locked(user))

    def test_trialing_user_is_never_locked(self):
        user = self._make_user("u_trial")
        Subscription.objects.create(user=user, status="trialing")
        self._make_entries(user, FREE_ENTRY_LIMIT + 25)

        self.assertFalse(is_free_locked(user))
