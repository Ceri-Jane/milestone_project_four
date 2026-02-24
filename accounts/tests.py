from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class ChangeUsernameTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="ceri",
            email="ceri@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="alreadytaken",
            email="other@example.com",
            password="testpass123",
        )

    def test_change_username_rejects_existing_username(self):
        """User cannot change username to one that is already taken."""
        self.client.login(username="ceri", password="testpass123")

        response = self.client.post(
            reverse("change_username"),
            {"username": "alreadytaken"},
            follow=True,
        )

        # Stays on the change username page (no redirect to profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/change_username.html")

        # Message is shown
        messages = list(response.context["messages"])
        self.assertTrue(any("already taken" in str(m).lower() for m in messages))

        # Username unchanged in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "ceri")
