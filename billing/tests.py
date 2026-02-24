from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Subscription


class RegulatePlusViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="ceri",
            email="ceri@example.com",
            password="testpass123",
        )

    def test_regulate_plus_sets_active_plan_flags_for_trialing(self):
        """
        If subscription is trialing, the page should flag the plan as active
        and reflect trial usage state.
        """
        Subscription.objects.create(
            user=self.user,
            status="trialing",
            has_had_trial=True,
        )

        self.client.login(username="ceri", password="testpass123")
        response = self.client.get(reverse("regulate_plus"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "billing/regulate_plus.html")

        self.assertIn("subscription", response.context)
        self.assertEqual(response.context["subscription_status"], "trialing")
        self.assertTrue(response.context["is_active_plan"])
        self.assertTrue(response.context["has_had_trial"])
