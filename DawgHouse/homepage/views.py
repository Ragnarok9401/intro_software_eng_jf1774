from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Bark, DawgHouseUser, SniffRequest
from .forms import CustomUserCreationForm, EditUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


def home_view(request):
    return render(request, "homepage.html")


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
        if user is not None:
            login(request, user)
            # right now this redirects to a landing page but this will need to be changed to the user's timeline later
            return redirect(f"/profile/{user.username}")
        else:
            message = "Unrecognized Dawgtag or Password"

        return render(request, "login.html", {"form": form, "message": message})

    return render(request, "login.html", {"form": form})


def signupView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            # for these redirects, put the URL path in there
            # for example, if we wanted to go to signup with would be "signup/"
            # for now upon successful recreation we will redirect home, which is path ""
            # we can change this later
            login(request, user)
            return redirect(f"/profile/{user.username}")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return redirect("/signup/")
    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def send_sniff_request(request, user_ID):
    from_user = request.user
    to_user = DawgHouseUser.objects.get(id=user_ID)
    sniff_request, created = SniffRequest.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        return HttpResponse("sniff request sent")
    else:
        return HttpResponse("sniff request was already sent")


@login_required
def accept_sniff_request(request, request_ID):
    sniff_request = SniffRequest.objects.get(id=request_ID)
    if sniff_request.to_user == request.user:
        sniff_request.to_user.friends.add(sniff_request.from_user)
        sniff_request.from_user.friends.add(sniff_request.to_user)
        sniff_request.delete()
        return HttpResponse("sniff request accepted")
    else:
        return HttpResponse("sniff request declined")


@login_required
def send_example_view(request):
    allusers = DawgHouseUser.objects.all()
    all_sniff_requests = SniffRequest.objects.all()

    context = {
        "allusers": allusers,
        "all_sniff_requests": all_sniff_requests,
    }
    return render(request, "sniff_example.html", context)


@login_required
def accept_example_view(request):
    all_sniff_requests = SniffRequest.objects.all()

    context = {
        "all_sniff_requests": all_sniff_requests,
    }
    return render(request, "accept_sniffs_example.html", context)


def ProfileView(request, username):
    user = get_object_or_404(DawgHouseUser, username=username)
    friends_list = user.friends.all()
    barks = Bark.objects.filter(user=user).order_by("-timestamp")
    context = {"user": user, "barks": barks, "friends_list": friends_list}
    return render(request, "user_profile.html", context)


def userEdit(request, username):
    user = get_object_or_404(DawgHouseUser, username=username)
    if request.method == "GET":
        form = EditUserForm(initial=model_to_dict(user))
        return render(request, "edit_user.html", {"form": form})
    elif request.method == "POST":
        user = get_object_or_404(DawgHouseUser, username=username)
        form = EditUserForm(request.POST)
        if form.is_valid():
            user.bio = form.cleaned_data["bio"]
            user.save()
            return redirect(f"/profile/{username}")
        else:
            return HttpResponseRedirect(reverse("some_fail_loc"))


@login_required
def post_bark(request):
    if request.method == "POST":
        bark_content = request.POST.get("bark_content")

        new_bark = Bark(user=request.user, content=bark_content)
        new_bark.save()

        return redirect(f"/profile/{request.user.username}/")

    return redirect("/")


@login_required
def give_treat(request, bark_id):
    bark = get_object_or_404(Bark, id=bark_id)
    bark.num_likes += 1
    bark.save()

    return redirect(f"/profile/{request.user.username}/")


@login_required
def give_treat(request, bark_id):
    bark = get_object_or_404(Bark, id=bark_id)
    user = request.user

    if user in bark.treated_by.all():
        bark.num_likes -= 1
        bark.treated_by.remove(user)
    else:
        bark.num_likes += 1
        bark.treated_by.add(user)

    bark.save()
    return redirect(f"/profile/{request.user.username}/")


@method_decorator(csrf_exempt, name="dispatch")
def edit_bio_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_bio = data.get("bio")
        request.user.bio = new_bio
        request.user.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
