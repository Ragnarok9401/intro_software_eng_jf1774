from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import DawgHouseUser
from .forms import CustomUserCreationForm, LoginForm

def home_view(request):
    return render(request, 'homepage.html')

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate (
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
        if user is not None:
            login(request, user)
            #right now this redirects to a landing page but this will need to be changed to the user's timeline later
            return redirect('/')
        else:
            message = 'Unrecognized Dawgtag or Password'

        return render(request, "login.html", {'form': form, 'message': message})
        
    return render(request, "login.html", {'form': form})

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
            return redirect('/signup/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

