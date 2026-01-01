from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """
    Display the logged-in user's profile page.
    This will become the main place to manage username, email and password.
    """
    return render(request, "account/profile.html")
