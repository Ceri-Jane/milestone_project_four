from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    error = None

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me") == "on"

        # If the user entered an email, convert to username
        try:
            if "@" in username_or_email:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            else:
                username = username_or_email
        except User.DoesNotExist:
            username = username_or_email  # fallback — will still fail safely

        # Authenticate normally
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            response = redirect("home")

            if remember_me:
                # Store the original email/username entered
                response.set_cookie("username", username_or_email, max_age=60*60*24*30)
            else:
                response.delete_cookie("username")

            return response

        # If login failed
        error = "Invalid username/email or password."

    return render(request, "accounts/login.html", {"error": error})
