from django.db import models
from django.contrib.auth.models import User  # built-in user model


class Entry(models.Model):
    """Single emotional entry for a logged-in user."""

    MOOD_CHOICES = [
        (1, "Very low"),
        (2, "Low"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Very good"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="entries",  # quick reverse lookup: user.entries.all()
    )
    mood = models.IntegerField(choices=MOOD_CHOICES)  # 1–5 mood rating
    hue = models.CharField(max_length=7, blank=True)  # HEX colour e.g. #a5dfc6
    emotion_words = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated emotion words.",  # short hint for admin form
    )
    notes = models.TextField(blank=True)  # optional free-text notes
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp on save

    class Meta:
        ordering = ["-created_at"]  # newest entries first

    def __str__(self):
        return f"{self.user.username} – {self.get_mood_display()} – {self.created_at:%Y-%m-%d}"
