from django.db import models
from django.contrib.auth.models import User  # built-in user model


class EmotionWord(models.Model):
    """
    Stores a single emotion word used as an option
    in the Emotion Words checkbox list on the entry form.
    """

    word = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["word"]
        verbose_name = "Emotion word"
        verbose_name_plural = "Emotion words"

    def __str__(self):
        return self.word


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
        related_name="entries",
    )

    mood = models.IntegerField(choices=MOOD_CHOICES)  # 1–5 mood rating
    hue = models.CharField(max_length=7, blank=True)  # HEX colour e.g. #a5dfc6

    emotion_words = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated emotion words.",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} – {self.get_mood_display()} – "
            f"{self.created_at:%Y-%m-%d}"
        )


class EntryRevision(models.Model):
    """
    Snapshot of an Entry before it was edited.
    """

    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name="revisions",
    )

    # 🔥 THIS is the key change — same choices as Entry
    mood = models.IntegerField(
        choices=Entry.MOOD_CHOICES,
        null=True,
        blank=True,
    )

    hue = models.CharField(max_length=7, blank=True)

    emotion_words = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated emotion words at the time of this revision.",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Revision of Entry {self.entry.id} at {self.created_at:%Y-%m-%d %H:%M}"
