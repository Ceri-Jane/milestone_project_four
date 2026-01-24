from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound

import random
import requests

from .models import Entry, EmotionWord, EntryRevision
from billing.models import Subscription


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
def new_entry(request):
    """
    Create a new entry.

    Notes:
    - Hue is stored as 0–100 (slider), then mapped to a simple 1–5 mood score.
    - Emotion words are stored as a comma-separated string for now (simple + fits CI scope).
    - Hue meaning + notes are combined into one text field so the UI stays low-friction.
    """
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

        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes}\n\n"
        if notes:
            combined_notes += notes

        Entry.objects.create(
            user=request.user,
            mood=mood,
            hue=hue,
            emotion_words=emotion_words,
            notes=combined_notes,
        )

        messages.success(request, "Your entry has been saved.")
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

    return render(
        request,
        "core/my_entries.html",
        {
            "grouped_entries": grouped_entries,
            "search_date": search_date,
        },
    )


@login_required
def dashboard(request):
    """Dashboard hub page."""
    subscription = Subscription.objects.filter(user=request.user).first()
    return render(request, "core/dashboard.html", {"subscription": subscription})


@login_required
def view_entry(request, entry_id):
    """Read-only entry view + revision history. Ownership is enforced."""
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
    revisions = EntryRevision.objects.filter(entry=entry).order_by("-created_at")
    last_updated = revisions[0].created_at if revisions else None

    return render(
        request,
        "core/entry_detail.html",
        {
            "entry": entry,
            "revisions": revisions,
            "last_updated": last_updated,
        },
    )


@login_required
def edit_entry(request, entry_id):
    """
    Edit an entry.

    Dev note:
    - Before saving changes, we snapshot the previous values into EntryRevision.
      This keeps the UI simple but still gives a clear audit trail of edits.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
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
            combined_notes += f"Hue meaning: {hue_notes}\n\n"
        if notes:
            combined_notes += notes

        has_changes = (
            entry.mood != mood
            or entry.hue != hue
            or entry.emotion_words != emotion_words
            or entry.notes != combined_notes
        )

        if has_changes:
            EntryRevision.objects.create(
                entry=entry,
                mood=entry.mood,
                hue=entry.hue,
                emotion_words=entry.emotion_words,
                notes=entry.notes,
            )

            entry.mood = mood
            entry.hue = hue
            entry.emotion_words = emotion_words
            entry.notes = combined_notes
            entry.save()

            messages.success(request, "Your entry has been updated.")
        else:
            messages.info(request, "No changes were made to your entry.")

        return redirect("my_entries")

    # GET: pre-fill form fields
    hue_value = entry.hue or ""
    hue_notes_value = ""
    notes_value = entry.notes or ""

    # Split "Hue meaning" out into its own field for the edit form
    if entry.notes and entry.notes.startswith("Hue meaning: "):
        parts = entry.notes.split("\n\n", 1)
        if len(parts) == 2:
            hue_notes_value = parts[0].replace("Hue meaning:", "", 1).strip()
            notes_value = parts[1]

    selected_emotions = []
    if entry.emotion_words:
        selected_emotions = [
            w.strip() for w in entry.emotion_words.split(",") if w.strip()
        ]

    return render(
        request,
        "core/entry_edit.html",
        {
            "entry": entry,
            "emotions": emotions,
            "hue_value": hue_value,
            "hue_notes_value": hue_notes_value,
            "notes_value": notes_value,
            "selected_emotions": selected_emotions,
        },
    )


@login_required
def delete_entry(request, entry_id):
    """Delete an entry (POST only)."""
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Your entry has been deleted.")
        return redirect("my_entries")

    messages.info(request, "Delete action was not completed.")
    return redirect("my_entries")


@login_required
def supportive_phrase(request):
    """
    Return a supportive phrase as JSON for the dashboard card.

    Dev notes:
    - We fetch server-side so it behaves the same locally + on deploy (and avoids CORS issues).
    - No session caching here on purpose: this API returns a single random affirmation and stays fresh.
    - If the API is down, we fall back to a small local set so the dashboard never looks broken.
    """
    fallback_quotes = [
        "Even on hard days, you deserve kindness from yourself.",
        "It’s okay to take things one small step at a time.",
        "You are allowed to rest without earning it first.",
        "Your feelings are valid, even when they are heavy.",
        "You are doing the best you can with what you have today.",
    ]

    try:
        # Returns JSON like: {"affirmation": "..." } (no API key needed)
        response = requests.get("https://www.affirmations.dev/", timeout=6)
        response.raise_for_status()

        data = response.json()
        quote = (data.get("affirmation") or "").strip()

        if not quote:
            raise ValueError("Affirmations.dev returned no affirmation text")

        return JsonResponse(
            {
                "quote": quote,
                "author": "Affirmations.dev",
            },
            status=200,
        )

    except Exception as e:
        # Keep this lightweight; useful while developing and harmless in production logs.
        print("Affirmations.dev API error:", e)

        return JsonResponse(
            {
                "quote": random.choice(fallback_quotes),
                "author": "Regulate",
            },
            status=200,
        )
