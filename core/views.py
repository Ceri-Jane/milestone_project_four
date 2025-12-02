from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Entry


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
    - Provides a fixed list of emotion words for checkboxes
    - Saves hue slider value, selected emotions, and notes
    """

    # Human-friendly timestamp for the template
    timestamp = timezone.localtime().strftime("%A %d %B %Y • %H:%M")

    # Emotion words shown as checkboxes on the form
    emotions = [
        "Agitated", "Alarmed", "Angry", "Anxious", "Ashamed",
        "Avoidant", "Blank", "Blue", "Brave", "Broken",
        "Calm", "Chaotic", "Cheerful", "Clingy", "Confident",
        "Conflicted", "Confused", "Connected", "Content", "Creative",
        "Critical", "Curious", "Defeated", "Defensive", "Depressed",
        "Detached", "Determined", "Disorganised", "Dissociated", "Distant",
        "Drained", "Dread", "Driven", "Empty", "Energetic",
        "Excited", "Exhausted", "Fidgety", "Foggy", "Fragile",
        "Frustrated", "Frozen", "Gentle", "Giddy", "Guilty",
        "Hopeless", "Hopeful", "Hostile", "Hyper", "Hyperfocused",
        "Hypervigilant", "Idealising", "Impatient", "Inattentive", "Indifferent",
        "Inspired", "Irritated", "Isolated", "Jittery", "Joyful",
        "Jumping", "Lonely", "Lost", "Low", "Motivated",
        "Nervous", "Neutral", "Numb", "Obsessed", "Optimistic",
        "Overloaded", "Overstimulated", "Overthinking", "Overwhelmed", "Panicky",
        "Peaceful", "Playful", "Present", "Proud", "Racing",
        "Relieved", "Rejected", "Restless", "Sad", "Safe",
        "Scared", "Scatterbrained", "Self-conscious", "Shaky", "Shame",
        "Shutdown", "Slow", "Soft", "Spaced-out", "Spiralling",
        "Stable", "Stressed", "Strong", "Supported", "Tense",
        "Tearful", "Tense", "Tired", "Trapped", "Triggered",
        "Uncertain", "Unfocused", "Unmotivated", "Unstable", "Unworthy",
        "Vulnerable", "Wired", "Worried"
    ]

    if request.method == "POST":
        # Get form values from POST
        hue = request.POST.get("hue")              # range slider value (0–100)
        notes = request.POST.get("notes")
        selected_emotions = request.POST.getlist("emotion_words")  # multiple checkboxes

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

        # Create the entry in the database
        Entry.objects.create(
            user=request.user,
            mood=mood,               # assumes mood can be null or 1–5
            hue=hue,
            emotion_words=emotion_words,
            notes=notes,
        )

        return redirect("home")  # dashboard for now

    # GET request: show empty form
    context = {
        "timestamp": timestamp,
        "emotions": emotions,
    }
    return render(request, "core/new_entry.html", context)
