from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.limits import FREE_ENTRY_LIMIT, is_free_locked
from core.models import Entry

User = get_user_model()


class TestDeleteUnlocksFreePlan(TestCase):
    """
    TDD: A free-plan user who hits the entry cap should still be able to delete
    an entry to reduce their count (and become unlocked again).

    This prevents users being trapped at the cap with no way to manage data.
    """

    def setUp(self):
        self.password = "pass12345!"

    def _create_and_login(self, username="freeuser"):
        user = User.objects.create_user(username=username, password=self.password)
        self.client.login(username=username, password=self.password)
        return user

    def _make_entries(self, user, count):
        Entry.objects.bulk_create(
            [Entry(user=user, mood=3, hue="50") for _ in range(count)]
        )

    def test_free_locked_user_can_delete_to_unlock(self):
        user = self._create_and_login("capuser")
        self._make_entries(user, FREE_ENTRY_LIMIT)

        self.assertTrue(is_free_locked(user))

        entry = Entry.objects.filter(user=user).first()
        delete_url = reverse("delete_entry", args=[entry.id])

        response = self.client.post(delete_url)

        # Expect normal delete behaviour (redirect back to entries list)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("my_entries"), response.url)

        # Entry should be deleted
        self.assertFalse(Entry.objects.filter(id=entry.id).exists())

        # User should now be below cap and unlocked
        self.assertEqual(Entry.objects.filter(user=user).count(), FREE_ENTRY_LIMIT - 1)
        self.assertFalse(is_free_locked(user))
