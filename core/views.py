from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Entry, EmotionWord, EntryRevision  # include revisions


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
    Show a single entry in read-only mode, plus its revision history.
    Ensures the entry belongs to the logged-in user.
    """
    entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
    revisions = EntryRevision.objects.filter(entry=entry).order_by("-created_at")

    context = {
        "entry": entry,
        "revisions": revisions,
    }
    return render(request, "core/entry_detail.html", context)


@login_required
def edit_entry(request, entry_id):
    """
    Allow the user to edit an existing entry.

    - Pre-populates the form with the current values
    - Before updating, stores a snapshot of the current values
      in EntryRevision so you can see how it has changed over time.
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

        # Check if anything actually changed
        has_changes = (
            entry.mood != mood
            or entry.hue != hue
            or entry.emotion_words != emotion_words
            or entry.notes != combined_notes
        )

        if has_changes:
            # Store previous state in revision history
            EntryRevision.objects.create(
                entry=entry,
                mood=entry.mood,
                hue=entry.hue,
                emotion_words=entry.emotion_words,
                notes=entry.notes,
            )

            # Update existing entry with new values
            entry.mood = mood
            entry.hue = hue
            entry.emotion_words = emotion_words
            entry.notes = combined_notes
            entry.save()

            messages.success(request, "Your entry has been updated.")
        else:
            messages.info(request, "No changes were made to your entry.")

        return redirect("dashboard")

    # ------------------------------
    # GET: pre-fill form fields
    # ------------------------------

    # 1) Hue slider value (we currently store 0–100 as text)
    hue_value = entry.hue or ""

    # 2) Split stored notes into "hue meaning" and main notes (best-effort)
    hue_notes_value = ""
    notes_value = entry.notes or ""

    if entry.notes and entry.notes.startswith("Hue meaning: "):
        parts = entry.notes.split("\n\n", 1)
        if len(parts) == 2:
            # First part after "Hue meaning:" prefix
            hue_notes_value = parts[0].replace("Hue meaning:", "", 1).strip()
            notes_value = parts[1]

    # 3) Selected emotion words as list
    selected_emotions = []
    if entry.emotion_words:
        selected_emotions = [
            w.strip() for w in entry.emotion_words.split(",") if w.strip()
        ]

    context = {
        "entry": entry,
        "emotions": emotions,
        "hue_value": hue_value,
        "hue_notes_value": hue_notes_value,
        "notes_value": notes_value,
        "selected_emotions": selected_emotions,
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
