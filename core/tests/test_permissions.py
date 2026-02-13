from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Entry


User = get_user_model()


class TestCorePermissions(TestCase):
    """Auth + ownership checks for entry routes and dashboard."""

    def setUp(self):
        self.password = "pass12345!"

    def _create_and_login(self, username):
        user = User.objects.create_user(username=username, password=self.password)
        self.client.login(username=username, password=self.password)
        return user

    def _make_entry(self, user, mood=3, hue="50", notes="secret"):
        """Create a minimal valid Entry owned by the given user."""
        return Entry.objects.create(user=user, mood=mood, hue=hue, notes=notes)

    def test_dashboard_requires_login_redirects_anonymous(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_cannot_view_another_users_entry(self):
        owner = User.objects.create_user(username="owner", password=self.password)
        self._create_and_login("intruder")

        entry = self._make_entry(owner)

        response = self.client.get(reverse("view_entry", args=[entry.id]))
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_another_users_entry(self):
        owner = User.objects.create_user(username="owner2", password=self.password)
        self._create_and_login("intruder2")

        entry = self._make_entry(owner)

        response = self.client.get(reverse("edit_entry", args=[entry.id]))
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_another_users_entry(self):
        owner = User.objects.create_user(username="owner3", password=self.password)
        self._create_and_login("intruder3")

        entry = self._make_entry(owner)

        response = self.client.post(reverse("delete_entry", args=[entry.id]))

        # Hidden-resource behaviour: treat as non-existent for non-owners
        self.assertEqual(response.status_code, 404)

        # Entry should still exist
        self.assertTrue(Entry.objects.filter(id=entry.id).exists())
