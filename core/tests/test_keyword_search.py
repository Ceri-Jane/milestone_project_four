from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Entry


User = get_user_model()


class TestKeywordSearch(TestCase):
    """Keyword search on My Entries (notes + emotion_words)."""

    def setUp(self):
        self.password = "pass12345!"
        self.user = User.objects.create_user(username="searchuser", password=self.password)
        self.client.login(username="searchuser", password=self.password)

    def test_search_filters_by_notes_and_emotion_words(self):
        Entry.objects.create(
            user=self.user,
            mood=3,
            hue="50",
            emotion_words="calm, grounded",
            notes="Walked the dog and felt steady.",
        )
        Entry.objects.create(
            user=self.user,
            mood=2,
            hue="30",
            emotion_words="anxious, overwhelmed",
            notes="Could not focus today.",
        )
        Entry.objects.create(
            user=self.user,
            mood=4,
            hue="70",
            emotion_words="happy",
            notes="Pizza night with a film.",
        )

        url = reverse("my_entries") + "?q=anxious"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Should include the matching entry
        self.assertContains(response, "anxious")

        # Should exclude non-matching content
        self.assertNotContains(response, "Pizza night with a film.")
        self.assertNotContains(response, "Walked the dog and felt steady.")
