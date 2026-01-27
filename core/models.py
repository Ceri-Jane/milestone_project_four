from django.db import models
from django.conf import settings
from django.utils import timezone


class EmotionWord(models.Model):
    """
    Single emotion word used as an option
    in the entry emotion selector.
    """
    word = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["word"]
        verbose_name = "Emotion word"
        verbose_name_plural = "Emotion words"

    def __str__(self):
        return self.word


class Entry(models.Model):
    """Single emotional entry created by a user."""

    MOOD_CHOICES = [
        (1, "Very low"),
        (2, "Low"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Very good"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    mood = models.IntegerField(choices=MOOD_CHOICES)
    hue = models.CharField(max_length=7, blank=True)

    # --------------------------------------------------
    # Original comma-separated emotion words (UX-friendly)
    # --------------------------------------------------
    emotion_words = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated emotion words.",
    )

    # --------------------------------------------------
    # Relational emotion word tags (for data modelling)
    # --------------------------------------------------
    emotion_word_tags = models.ManyToManyField(
        EmotionWord,
        blank=True,
        related_name="entries",
        help_text="Relational emotion word tags linked to this entry.",
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    def __str__(self):
        return (
            f"{self.user.username} – {self.get_mood_display()} – "
            f"{self.created_at:%Y-%m-%d}"
        )


class EntryRevision(models.Model):
    """Snapshot of an entry before it was edited."""

    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name="revisions",
    )

    mood = models.IntegerField(
        choices=Entry.MOOD_CHOICES,
        null=True,
        blank=True,
    )

    hue = models.CharField(max_length=7, blank=True)

    emotion_words = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated emotion words at time of edit.",
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Entry revision"
        verbose_name_plural = "Entry revisions"

    def __str__(self):
        return f"Revision of Entry {self.entry.id} at {self.created_at:%Y-%m-%d %H:%M}"


class SiteAnnouncement(models.Model):
    """
    Short site-wide announcements (e.g. maintenance or updates).
    Contains no private user content.
    """
    title = models.CharField(max_length=120)
    message = models.TextField(max_length=600)

    is_active = models.BooleanField(default=True)

    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_live(self):
        if not self.is_active:
            return False

        now = timezone.now()

        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False

        return True

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    """
    Simple support inbox for user contact.
    Intended for account or site queries only.
    """

    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("resolved", "Resolved"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_tickets",
        help_text="Set if the user was logged in.",
    )

    email = models.EmailField(blank=True, help_text="Used if the user is logged out.")
    subject = models.CharField(max_length=140)
    message = models.TextField(max_length=3000)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        who = self.user.username if self.user else (self.email or "Unknown")
        return f"{self.subject} ({who})"
