from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import DawgHouseUser
from .forms import CustomUserCreationForm

def home(request):
    return render(request, "index.html")

def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect('/')
        else:
            for message in form.errors.values():
                messages.error(request, message[0])
            return redirect('signup')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

