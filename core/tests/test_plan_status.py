from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from billing.models import Subscription


User = get_user_model()


class TestPlanBannerRendering(TestCase):
    """
    Banner lives in base.html and is driven by core/context_processors.plan_status.

    Test via GET /dashboard/ to verify real template output (not just logic).
    """

    def setUp(self):
        self.url = reverse("dashboard")
        self.password = "pass12345!"

    def _login_user(self, username="user"):
        """Create + login a user for template-based banner assertions."""
        user = User.objects.create_user(username=username, password=self.password)
        self.client.login(username=username, password=self.password)
        return user

    def test_free_user_sees_free_plan_banner(self):
        self._login_user("freeuser")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Free plan")
        self.assertContains(response, 'plan-banner plan-free')

    def test_trialing_status_user_sees_trial_banner(self):
        user = self._login_user("trialinguser")
        Subscription.objects.create(user=user, status="trialing")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Regulate+ free trial")
        self.assertContains(response, 'plan-banner plan-trial')

    def test_trial_end_in_future_user_sees_trial_banner(self):
        user = self._login_user("trialenduser")
        Subscription.objects.create(
            user=user,
            status="incomplete",
            trial_end=timezone.now() + timedelta(days=7),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Regulate+ free trial")
        self.assertContains(response, 'plan-banner plan-trial')

    def test_active_subscription_user_sees_plus_banner(self):
        user = self._login_user("plususer")
        Subscription.objects.create(user=user, status="active")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Regulate+ subscription")
        self.assertContains(response, 'plan-banner plan-plus')

    def test_period_end_in_future_user_sees_ending_soon_banner(self):
        user = self._login_user("endinguser")
        Subscription.objects.create(
            user=user,
            status="canceled",
            current_period_end=timezone.now() + timedelta(days=3),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Regulate+ (ending soon)")
        self.assertContains(response, 'plan-banner plan-ending')
