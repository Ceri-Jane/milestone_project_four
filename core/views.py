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
    """Home page."""
    return render(request, "core/home.html")


def faq(request):
    """FAQ page."""
    try:
        return render(request, "pages/faq.html")
    except Exception:
        return HttpResponseNotFound("FAQ page not created yet.")


def support(request):
    """Crisis/support page."""
    try:
        return render(request, "pages/support.html")
    except Exception:
        return HttpResponseNotFound("Support page not created yet.")


@login_required
def contact(request):
    """Create a SupportTicket from the contact form."""
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
    """Create a new entry."""
    # Free plan gating: view-only after FREE_ENTRY_LIMIT entries
    if is_free_locked(request.user):
        messages.info(
            request,
            f"You’ve reached the free limit of {FREE_ENTRY_LIMIT} entries. "
            "You can still view your entries, but creating and editing is paused on the free plan."
        )
        return redirect("my_entries")

    timestamp = timezone.localtime().strftime("%A %d %B %Y • %H:%M")
    emotions = EmotionWord.objects.all()

    if request.method == "POST":
        # Form values
        hue = request.POST.get("hue")
        hue_notes = request.POST.get("hue_notes")
        notes = request.POST.get("notes")
        selected_emotions = request.POST.getlist("emotion_words")

        # Map hue slider (0–100) to mood score (1–5)
        mood = None
        hue_value = None
        if hue:
            try:
                hue_value = int(hue)
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None
                hue_value = None

        # Store emotion words as a simple CSV string
        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        # Combine hue meaning + notes into one notes field
        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
        if notes:
            combined_notes += notes.strip()

        Entry.objects.create(
            user=request.user,
            hue=hue_value,
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
    """List entries grouped by date, with optional date filter."""
    user_entries = Entry.objects.filter(user=request.user).order_by("-created_at")

    # Optional ?date=YYYY-MM-DD filter
    search_date = request.GET.get("date")
    if search_date:
        user_entries = user_entries.filter(created_at__date=search_date)

    # Group entries by date for accordion display
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

    # Active announcements filtered by live window
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
    """Entry detail view with revision history."""
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
    """Edit an entry and store a revision snapshot."""
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)

    # Free plan gating
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
        hue_value = None
        if hue:
            try:
                hue_value = int(hue)
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None
                hue_value = None

        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
        if notes:
            combined_notes += notes.strip()

        # Save previous values before overwrite
        EntryRevision.objects.create(
            entry=entry,
            previous_hue=entry.hue,
            previous_mood=entry.mood,
            previous_emotion_words=entry.emotion_words,
            previous_notes=entry.notes,
        )

        entry.hue = hue_value
        entry.mood = mood
        entry.emotion_words = emotion_words
        entry.notes = combined_notes
        entry.save()

        messages.success(request, "Entry updated.")
        return redirect("view_entry", entry_id=entry.id)

    # Prefill fields from combined notes format
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
        selected_emotions = [
            e.strip() for e in entry.emotion_words.split(",") if e.strip()
        ]

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

    # Free plan gating
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
    """Return a supportive phrase for the dashboard (AJAX)."""
    fallback_phrases = [
        "You’re allowed to take today slowly.",
        "Small steps count — even tiny ones.",
        "You don’t have to earn rest.",
        "Try naming one feeling without judging it.",
        "It’s okay to pause. You can come back when you’re ready.",
        "Your feelings are real — and they can change.",
        "One kind thing for yourself is enough for now.",
    ]

    phrase = None
    author = ""

    # External API: {"affirmation": "..."}
    try:
        r = requests.get("https://www.affirmations.dev/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            phrase = data.get("affirmation")
            if phrase:
                author = "Affirmations.dev"
    except Exception:
        phrase = None
        author = ""

    # Fallback if API fails/returns nothing
    if not phrase:
        phrase = random.choice(fallback_phrases)
        author = ""

    response = JsonResponse(
        {
            "quote": phrase,   # backwards compatibility
            "phrase": phrase,
            "author": author,
        }
    )

    # Prevent caching for repeated fetches
    response["Cache-Control"] = "no-store"
    return response
