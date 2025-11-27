from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry


def home(request):
    """Dashboard / landing page."""
    return render(request, "core/home.html")


@login_required
def new_entry(request):
    """Create a new mood entry."""
    if request.method == "POST":
        mood = request.POST.get("mood")
        hue = request.POST.get("hue")
        emotion_words = request.POST.get("emotion_words")
        notes = request.POST.get("notes")

        Entry.objects.create(
            user=request.user,
            mood=mood,
            hue=hue,
            emotion_words=emotion_words,
            notes=notes,
        )

        return redirect("home")  # dashboard for now

    return render(request, "core/new_entry.html")
