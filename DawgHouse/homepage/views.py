from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import DawgHouseUser
from .forms import CustomUserCreationForm

def login(request):
    return render(request, "login.html")

def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully')
            # for these redirects, put the URL path in there
            # for example, if we wanted to go to signup with would be "signup/"
            # for now upon successful recreation we will redirect home, which is path ""
            # we can change this later
            return redirect('/')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return redirect('signup')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

