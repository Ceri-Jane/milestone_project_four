from django.shortcuts import render

def home(request):
    """
    Temporary placeholder home view.
    This will eventually become the main dashboard.
    """
    return render(request, "core/home.html")
