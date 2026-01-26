from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound

import random
import requests

from .models import (
    Entry,
    EmotionWord,
    EntryRevision,
    SupportTicket,
    SiteAnnouncement,
)
from billing.models import Subscription
from .limits import is_free_locked, user_entry_count, FREE_ENTRY_LIMIT


def home(request):
    """Landing page."""
    return render(request, "core/home.html")


def faq(request):
    """Static FAQ page."""
    try:
        return render(request, "pages/faq.html")
    except Exception:
        return HttpResponseNotFound("FAQ page not created yet.")


def support(request):
    """Static crisis/support info page."""
    try:
        return render(request, "pages/support.html")
    except Exception:
        return HttpResponseNotFound("Support page not created yet.")


@login_required
def contact(request):
    """Simple contact form that creates a SupportTicket."""
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not subject or not message:
            messages.error(request, "Please fill in both the subject and message.")
            return redirect("contact")

        SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            message=message,
        )

        messages.success(request, "Message sent. Thank you — we’ll reply when we can.")
        return redirect("contact")

    return render(request, "pages/contact.html")


@login_required
def new_entry(request):
    """
    Create a new entry.

    Notes:
    - Hue is stored as 0–100 (slider), then mapped to a simple 1–5 mood score.
    - Emotion words are stored as a comma-separated string for now (simple + fits CI scope).
    - Hue meaning + notes are combined into one text field so the UI stays low-friction.
    """
    # Free plan gating: 10 entries total, then view-only
    if is_free_locked(request.user):
        messages.info(
            request,
            f"You’ve reached the free limit of {FREE_ENTRY_LIMIT} entries. "
            "You can still view your entries, but creating and editing is paused on the free plan."
        )
        return redirect("my_entries")

    timestamp = timezone.localtime().strftime("%A %d %B %Y • %H:%M")
    emotions = EmotionWord.objects.all()  # ordered via model Meta

    if request.method == "POST":
        hue = request.POST.get("hue")  # 0–100
        hue_notes = request.POST.get("hue_notes")
        notes = request.POST.get("notes")
        selected_emotions = request.POST.getlist("emotion_words")

        mood = None
        if hue:
            try:
                hue_value = int(hue)
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None

        # Store selected emotions as comma-separated string
        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        # Combine hue meaning + notes into one text field
        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
        if notes:
            combined_notes += notes.strip()

        Entry.objects.create(
            user=request.user,
            hue=hue_value if hue else None,
            mood=mood,
            emotion_words=emotion_words,
            notes=combined_notes,
        )

        messages.success(request, "Entry saved.")
        return redirect("my_entries")

    return render(
        request,
        "core/new_entry.html",
        {
            "timestamp": timestamp,
            "emotions": emotions,
        },
    )


@login_required
def my_entries(request):
    """
    User entries page (grouped by date, not a calendar).

    UX intent:
    - Avoid “empty days” and pressure to keep streaks.
    - Optional date filter via ?date=YYYY-MM-DD.
    """
    user_entries = Entry.objects.filter(user=request.user).order_by("-created_at")

    search_date = request.GET.get("date")
    if search_date:
        user_entries = user_entries.filter(created_at__date=search_date)

    grouped_entries = {}
    for entry in user_entries:
        entry.has_revisions = entry.revisions.exists()
        date_key = entry.created_at.date()
        grouped_entries.setdefault(date_key, []).append(entry)

    entry_count = user_entry_count(request.user)
    locked = is_free_locked(request.user)

    return render(
        request,
        "core/my_entries.html",
        {
            "grouped_entries": grouped_entries,
            "search_date": search_date,
            "is_free_locked": locked,
            "entry_count": entry_count,
            "free_entry_limit": FREE_ENTRY_LIMIT,
        },
    )


@login_required
def dashboard(request):
    """Dashboard hub page."""
    subscription = Subscription.objects.filter(user=request.user).first()

    # Pull active announcements then apply "live window" logic in Python
    active_announcements = SiteAnnouncement.objects.filter(is_active=True).order_by(
        "-updated_at"
    )
    live_announcements = [a for a in active_announcements if a.is_live]

    entry_count = user_entry_count(request.user)
    locked = is_free_locked(request.user)

    return render(
        request,
        "core/dashboard.html",
        {
            "subscription": subscription,
            "announcements": live_announcements,
            "is_free_locked": locked,
            "entry_count": entry_count,
            "free_entry_limit": FREE_ENTRY_LIMIT,
        },
    )


@login_required
def view_entry(request, entry_id):
    """Read-only entry view + revision history. Ownership is enforced."""
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
    revisions = EntryRevision.objects.filter(entry=entry).order_by("-created_at")
    last_updated = revisions[0].created_at if revisions else None
    locked = is_free_locked(request.user)

    return render(
        request,
        "core/entry_detail.html",
        {
            "entry": entry,
            "revisions": revisions,
            "last_updated": last_updated,
            "is_free_locked": locked,
        },
    )


@login_required
def edit_entry(request, entry_id):
    """
    Edit an entry.

    Dev note:
    - Before saving changes, snapshot the previous values into EntryRevision.
      This keeps the UI simple but still gives a clear audit trail of edits.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)

    if is_free_locked(request.user):
        messages.info(
            request,
            "Editing is paused on the free plan once you reach the 10 entry limit. "
            "You can still view your entries."
        )
        return redirect("view_entry", entry_id=entry.id)

    emotions = EmotionWord.objects.all()

    if request.method == "POST":
        hue = request.POST.get("hue")
        hue_notes = request.POST.get("hue_notes")
        notes = request.POST.get("notes")
        selected_emotions = request.POST.getlist("emotion_words")

        mood = None
        if hue:
            try:
                hue_value = int(hue)
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None

        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
        if notes:
            combined_notes += notes.strip()

        # Snapshot existing values before overwriting
        EntryRevision.objects.create(
            entry=entry,
            previous_hue=entry.hue,
            previous_mood=entry.mood,
            previous_emotion_words=entry.emotion_words,
            previous_notes=entry.notes,
        )

        entry.hue = hue_value if hue else None
        entry.mood = mood
        entry.emotion_words = emotion_words
        entry.notes = combined_notes
        entry.save()

        messages.success(request, "Entry updated.")
        return redirect("view_entry", entry_id=entry.id)

    # Prefill fields
    existing_hue_notes = ""
    existing_notes = entry.notes or ""
    if existing_notes.startswith("Hue meaning:"):
        try:
            parts = existing_notes.split("\n\n", 1)
            existing_hue_notes = parts[0].replace("Hue meaning:", "").strip()
            existing_notes = parts[1] if len(parts) > 1 else ""
        except Exception:
            pass

    selected_emotions = []
    if entry.emotion_words:
        selected_emotions = [e.strip() for e in entry.emotion_words.split(",") if e.strip()]

    return render(
        request,
        "core/edit_entry.html",
        {
            "entry": entry,
            "emotions": emotions,
            "existing_hue_notes": existing_hue_notes,
            "existing_notes": existing_notes,
            "selected_emotions": selected_emotions,
        },
    )


@login_required
def delete_entry(request, entry_id):
    """Delete an entry (POST only)."""
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)

    if is_free_locked(request.user):
        messages.info(
            request,
            "Deleting is paused on the free plan once you reach the 10 entry limit. "
            "You can still view your entries."
        )
        return redirect("my_entries")

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Your entry has been deleted.")
        return redirect("my_entries")

    messages.info(request, "Delete action was not completed.")
    return redirect("my_entries")


@login_required
def supportive_phrase(request):
    """
    Returns a supportive phrase for the UI.
    - Intended for AJAX fetch from dashboard card/button.
    - Keeps tone gentle and optional.
    """
    phrases = [
        "You’re allowed to take today slowly.",
        "Small steps count — even tiny ones.",
        "You don’t have to earn rest.",
        "Try naming one feeling without judging it.",
        "It’s okay to pause. You can come back when you’re ready.",
        "Your feelings are real — and they can change.",
        "One kind thing for yourself is enough for now.",
    ]
    return JsonResponse({"phrase": random.choice(phrases)})
