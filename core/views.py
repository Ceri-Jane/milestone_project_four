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
from .forms import EntryForm  # Entry create/edit ModelForm
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
        return HttpResponseNotFound("FAQ page not created yet.")


def contact(request):
    """Create a SupportTicket from the contact form (public page)."""
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Only required when the user is logged out
        email = request.POST.get("email", "").strip().lower()

        if not subject or not message:
            messages.error(request, "Please fill in both the subject and message.")
            return redirect("contact")

        if not request.user.is_authenticated and not email:
            messages.error(request, "Please provide an email address so we can reply.")
            return redirect("contact")

        SupportTicket.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email if not request.user.is_authenticated else "",
            subject=subject,
            message=message,
        )

        messages.success(request, "Message sent. Thank you — we’ll reply when we can.")
        return redirect("contact")

    return render(request, "pages/contact.html")


@login_required
def new_entry(request):
    """Create a new entry."""
    if is_free_locked(request.user):
        messages.info(
            request,
            f"You’ve reached the free limit of {FREE_ENTRY_LIMIT} entries. "
            "You can still view your entries, but creating and editing is paused on the free plan."
        )
        return redirect("my_entries")

    timestamp = timezone.localtime().strftime("%A %d %B %Y • %H:%M")
    emotions = EmotionWord.objects.all()

    # Use ModelForm for server-side validation
    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            hue_notes = request.POST.get("hue_notes")
            notes = request.POST.get("notes")

            # Templates submit checkboxes as name="emotion_words"
            selected_words = request.POST.getlist("emotion_words")

            # Defaults so Entry.mood never ends up None
            mood = 3
            hue_value = 50

            # Hue is cleaned in the form, but we still clamp + compute mood here
            hue = form.cleaned_data.get("hue")
            if hue not in (None, ""):
                try:
                    hue_value = int(hue)
                    hue_value = max(0, min(100, hue_value))
                    mood = max(1, min(5, (hue_value // 20) + 1))
                except (TypeError, ValueError):
                    pass

            combined_notes = ""
            if hue_notes:
                combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
            if notes:
                combined_notes += notes.strip()

            entry = form.save(commit=False)
            entry.user = request.user
            entry.hue = str(hue_value)
            entry.mood = mood
            entry.notes = combined_notes

            # Keep comma-separated field in sync for display/backwards compatibility
            entry.emotion_words = ", ".join(selected_words) if selected_words else ""

            entry.save()

            # Sync relational tags (ManyToMany)
            if selected_words:
                objs = []
                for w in selected_words:
                    obj, _ = EmotionWord.objects.get_or_create(word=w)
                    objs.append(obj)
                entry.emotion_word_tags.set(objs)
            else:
                entry.emotion_word_tags.clear()

            messages.success(request, "Entry saved.")
            return redirect("my_entries")

        messages.error(request, "Please check the form and try again.")
        return redirect("new_entry")

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

    # Determine plan state for template (keeps dashboard logic clean + assessor-friendly)
    sub_status = getattr(subscription, "status", None)
    is_active_plan = sub_status in ["trialing", "active"]
    has_had_trial = getattr(subscription, "has_had_trial", False)

    active_announcements = SiteAnnouncement.objects.filter(is_active=True).order_by(
        "-updated_at"
    )
    live_announcements = [a for a in active_announcements if a.is_live]

    entry_count = user_entry_count(request.user)
    locked = is_free_locked(request.user)

    # --------------------------------------------------
    # Per-login key for dismissible dashboard alerts
    # --------------------------------------------------
    login_key = ""
    if request.user.last_login:
        login_key = request.user.last_login.isoformat()

    return render(
        request,
        "core/dashboard.html",
        {
            "subscription": subscription,
            "subscription_status": sub_status,
            "is_active_plan": is_active_plan,
            "has_had_trial": has_had_trial,

            "announcements": live_announcements,
            "is_free_locked": locked,
            "entry_count": entry_count,
            "free_entry_limit": FREE_ENTRY_LIMIT,
            "login_key": login_key,
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

    if is_free_locked(request.user):
        messages.info(
            request,
            "Editing is paused on the free plan once you reach the 10 entry limit. "
            "You can still view your entries."
        )
        return redirect("view_entry", entry_id=entry.id)

    emotions = EmotionWord.objects.all()

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)

        if form.is_valid():
            hue_notes = request.POST.get("hue_notes")
            notes = request.POST.get("notes")

            # Templates submit checkboxes as name="emotion_words"
            selected_words = request.POST.getlist("emotion_words")

            # Start with current values, only overwrite if the POST value is valid
            mood = entry.mood
            hue_value = entry.hue

            hue = form.cleaned_data.get("hue")
            if hue not in (None, ""):
                try:
                    hv = int(hue)
                    hv = max(0, min(100, hv))
                    hue_value = hv
                    mood = max(1, min(5, (hv // 20) + 1))
                except (TypeError, ValueError):
                    pass

            combined_notes = ""
            if hue_notes:
                combined_notes += f"Hue meaning: {hue_notes.strip()}\n\n"
            if notes:
                combined_notes += notes.strip()

            # Save previous values before overwrite (fields match EntryRevision model)
            EntryRevision.objects.create(
                entry=entry,
                hue=entry.hue,
                mood=entry.mood,
                emotion_words=entry.emotion_words,
                notes=entry.notes,
            )

            updated_entry = form.save(commit=False)
            updated_entry.hue = str(hue_value) if hue_value is not None else ""
            updated_entry.mood = mood
            updated_entry.notes = combined_notes

            # Keep comma-separated field in sync for display/backwards compatibility
            updated_entry.emotion_words = ", ".join(selected_words) if selected_words else ""

            updated_entry.save()

            # Sync relational tags (ManyToMany)
            if selected_words:
                objs = []
                for w in selected_words:
                    obj, _ = EmotionWord.objects.get_or_create(word=w)
                    objs.append(obj)
                updated_entry.emotion_word_tags.set(objs)
            else:
                updated_entry.emotion_word_tags.clear()

            messages.success(request, "Entry updated.")
            return redirect("view_entry", entry_id=entry.id)

        messages.error(request, "Please check the form and try again.")
        return redirect("edit_entry", entry_id=entry.id)

    # Split out hue meaning from saved notes (so the UI can edit it separately)
    existing_hue_notes = ""
    existing_notes = entry.notes or ""

    if existing_notes.startswith("Hue meaning:"):
        try:
            parts = existing_notes.split("\n\n", 1)
            existing_hue_notes = parts[0].replace("Hue meaning:", "").strip()
            existing_notes = parts[1] if len(parts) > 1 else ""
        except Exception:
            pass

    # Pre-select checkboxes in the template
    selected_emotions = list(entry.emotion_word_tags.values_list("word", flat=True))

    return render(
        request,
        "core/entry_edit.html",
        {
            "entry": entry,
            "emotions": emotions,
            "selected_emotions": selected_emotions,

            # Matches template variables
            "hue_value": int(entry.hue) if str(entry.hue).isdigit() else 50,
            "hue_notes_value": existing_hue_notes,
            "notes_value": existing_notes,
            "existing_hue_notes": existing_hue_notes,
            "existing_notes": existing_notes,
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

    if not phrase:
        phrase = random.choice(fallback_phrases)
        author = ""

    response = JsonResponse(
        {
            "quote": phrase,
            "phrase": phrase,
            "author": author,
        }
    )
    response["Cache-Control"] = "no-store"
    return response
