from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, "index.html")

def profile(request):
    return HttpResponse("Profile")  #example to show profile page works
