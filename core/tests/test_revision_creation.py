from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Entry

User = get_user_model()


class TestRevisionCreationLogic(TestCase):
    """Revisions should only be created when entry data actually changes."""

    def setUp(self):
        self.password = "pass12345!"

    def _create_and_login(self):
        user = User.objects.create_user(username="editor", password=self.password)
        self.client.login(username="editor", password=self.password)
        return user

    def test_edit_with_no_changes_does_not_create_revision(self):
        user = self._create_and_login()

        entry = Entry.objects.create(
            user=user,
            mood=3,
            hue="50",
            emotion_words="calm",
            notes="unchanged",
        )

        url = reverse("edit_entry", args=[entry.id])

        # Submit identical data (no change)
        response = self.client.post(url, {
            "mood": 3,
            "hue": "50",
            "emotion_words": "calm",
            "notes": "unchanged",
        })

        self.assertEqual(response.status_code, 302)

        # Expect: no revision created if nothing changed
        entry.refresh_from_db()
        self.assertEqual(entry.revisions.count(), 0)
