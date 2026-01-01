from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model


@login_required
def profile(request):
    """
    Display the logged-in user's profile page.
    This is the main place to manage username, email and password.
    """
    return render(request, "account/profile.html")


@login_required
def change_username(request):
    """
    Allow the logged-in user to update their username.
    """
    User = get_user_model()

    if request.method == "POST":
        new_username = request.POST.get("username", "").strip()

        # Basic validation
        if not new_username:
            messages.error(request, "Please enter a username.")
            return redirect("change_username")

        # Check if username is already taken by another user
        if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
            messages.error(request, "That username is already taken.")
            return redirect("change_username")

        # Update and save
        request.user.username = new_username
        request.user.save()

        messages.success(request, "Your username has been updated.")
        return redirect("profile")

    # GET: show form with current username pre-filled
    context = {
        "current_username": request.user.username,
    }
    return render(request, "account/change_username.html", context)
