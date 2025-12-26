from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Entry, EmotionWord  # import both models


def home(request):
    """
    Dashboard / landing page.
    For now this just renders the home template.
    Later this can show recent entries or stats.
    """
    return render(request, "core/home.html")


@login_required
def new_entry(request):
    """
    Display the New Entry form and handle saving an entry.

    - Shows a timestamp at the top of the form
    - Pulls emotion word options from EmotionWord model
    - Saves hue slider value, selected emotions, and notes
    """

    # Human-friendly timestamp for the template
    timestamp = timezone.localtime().strftime("%A %d %B %Y • %H:%M")

    # Pull emotion words from database (alphabetical from model.Meta)
    emotions = EmotionWord.objects.all()

    if request.method == "POST":
        # Get form values from POST
        hue = request.POST.get("hue")                 # range slider value (0–100)
        hue_notes = request.POST.get("hue_notes")     # meaning of hue
        notes = request.POST.get("notes")

        selected_emotions = request.POST.getlist("emotion_words")

        # Derive a simple 1–5 mood score from the hue slider
        mood = None
        if hue:
            try:
                hue_value = int(hue)
                # Map 0–100 into 1–5
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None

        # Join selected emotion words into a single string
        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        # Combine hue meaning + notes into a single text field
        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes}\n\n"
        if notes:
            combined_notes += notes

        # Create the entry in the database
        Entry.objects.create(
            user=request.user,
            mood=mood,
            hue=hue,
            emotion_words=emotion_words,
            notes=combined_notes,
        )

        # SUCCESS MESSAGE
        messages.success(request, "Your entry has been saved.")

        return redirect("home")  # dashboard for now

    # GET request: show empty form
    context = {
        "timestamp": timestamp,
        "emotions": emotions,
    }
    return render(request, "core/new_entry.html", context)


@login_required
def dashboard(request):
    """
    Show the logged-in user's entries in a grouped, non-calendar view.

    - Groups entries by date (no empty 'missing' days shown)
    - Optional filter: search by specific date via ?date=YYYY-MM-DD
    """
    # Base queryset: only this user's entries, newest first
    user_entries = Entry.objects.filter(user=request.user).order_by("-created_at")

    # Optional: filter by a specific date (string in YYYY-MM-DD format)
    search_date = request.GET.get("date")
    if search_date:
        user_entries = user_entries.filter(created_at__date=search_date)

    # Group entries by date for accordion display
    grouped_entries = {}
    for entry in user_entries:
        date_key = entry.created_at.date()
        grouped_entries.setdefault(date_key, []).append(entry)

    context = {
        "grouped_entries": grouped_entries,
        "search_date": search_date,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def view_entry(request, entry_id):
    """
    Show a single entry in read-only mode.
    Ensures the entry belongs to the logged-in user.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
    return render(request, "core/entry_detail.html", {"entry": entry})


@login_required
def edit_entry(request, entry_id):
    """
    Allow the user to edit an existing entry.
    Reuses the same basic logic as creating an entry.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
    emotions = EmotionWord.objects.all()

    if request.method == "POST":
        hue = request.POST.get("hue")
        hue_notes = request.POST.get("hue_notes")
        notes = request.POST.get("notes")
        selected_emotions = request.POST.getlist("emotion_words")

        # Derive mood from hue
        mood = None
        if hue:
            try:
                hue_value = int(hue)
                mood = max(1, min(5, (hue_value // 20) + 1))
            except ValueError:
                mood = None

        # Join selected emotion words into a single string
        emotion_words = ", ".join(selected_emotions) if selected_emotions else ""

        # Combine hue meaning + notes into a single text field
        combined_notes = ""
        if hue_notes:
            combined_notes += f"Hue meaning: {hue_notes}\n\n"
        if notes:
            combined_notes += notes

        # Update existing entry
        entry.mood = mood
        entry.hue = hue
        entry.emotion_words = emotion_words
        entry.notes = combined_notes
        entry.save()

        messages.success(request, "Your entry has been updated.")
        return redirect("dashboard")

    # GET: pre-fill form fields from the existing entry
    context = {
        "entry": entry,
        "emotions": emotions,
        # Can't perfectly split hue meaning from notes, so just pass full notes
        "existing_notes": entry.notes,
    }
    return render(request, "core/entry_edit.html", context)


@login_required
def delete_entry(request, entry_id):
    """
    Ask for confirmation, then delete an entry.
    Uses POST to actually delete.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Your entry has been deleted.")
        return redirect("dashboard")

    return render(request, "core/entry_confirm_delete.html", {"entry": entry})
