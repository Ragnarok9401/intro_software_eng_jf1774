from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def signupView(request):
    # logic
    return render(request, "signup/signup.html")
