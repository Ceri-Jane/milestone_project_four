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


@login_required
def change_email(request):
    """
    Allow the logged-in user to update their email address.
    """
    User = get_user_model()

    if request.method == "POST":
        new_email = request.POST.get("email", "").strip().lower()

        # Basic validation
        if not new_email:
            messages.error(request, "Please enter an email address.")
            return redirect("change_email")

        # Check if email already belongs to another account
        if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
            messages.error(request, "That email address is already in use.")
            return redirect("change_email")

        # Update and save
        request.user.email = new_email
        request.user.save()

        messages.success(request, "Your email address has been updated.")
        return redirect("profile")

    # GET — show current email in form
    context = {
        "current_email": request.user.email or "",
    }
    return render(request, "account/change_email.html", context)
