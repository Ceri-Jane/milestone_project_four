from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from billing.models import Subscription


@login_required
def profile(request):
    """
    Logged-in user's profile page.
    Keep account settings (username/email/password) and billing in one place.
    """
    subscription = Subscription.objects.filter(user=request.user).first()
    return render(request, "account/profile.html", {"subscription": subscription})


@login_required
def change_username(request):
    """Allow the logged-in user to update their username."""
    User = get_user_model()

    if request.method == "POST":
        new_username = request.POST.get("username", "").strip()

        if not new_username:
            messages.error(request, "Please enter a username.")
            return redirect("change_username")

        if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
            messages.error(request, "That username is already taken.")
            return redirect("change_username")

        request.user.username = new_username
        request.user.save()

        messages.success(request, "Your username has been updated.")
        return redirect("profile")

    return render(
        request,
        "account/change_username.html",
        {"current_username": request.user.username},
    )


@login_required
def change_email(request):
    """Allow the logged-in user to update their email address."""
    User = get_user_model()

    if request.method == "POST":
        new_email = request.POST.get("email", "").strip().lower()

        if not new_email:
            messages.error(request, "Please enter an email address.")
            return redirect("change_email")

        if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
            messages.error(request, "That email address is already in use.")
            return redirect("change_email")

        request.user.email = new_email
        request.user.save()

        messages.success(request, "Your email address has been updated.")
        return redirect("profile")

    return render(
        request,
        "account/change_email.html",
        {"current_email": request.user.email or ""},
    )
