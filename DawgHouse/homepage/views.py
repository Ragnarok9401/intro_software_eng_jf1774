"""
Contains views for DawgHouse
"""

# pylint: disable=no-member
# pylint: disable=undefined-variable

import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from Levenshtein import distance
from .models import Bark, DawgHouseUser, SniffRequest, Comment
from .forms import LoginForm, CustomUserCreationForm


def home_view(request):
    """Shows login/signup if not authenticated otherwise timeline"""
    if request.user.is_authenticated:
        user = request.user
        friends = user.friends.all()
        barks = Bark.objects.filter(Q(user=user) | Q(user__in=friends)).order_by(
            "-timestamp"
        )

        context = {
            "barks": barks,
        }

        return render(request, "main_page.html", context)

    return render(request, "homepage.html")


def login_view(request):
    """Handles loging form POST data"""
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
            return redirect("/main/")
        
        message = "Unrecognized Dawgtag or Password"

        return render(request, "login.html", {"form": form, "message": message})

    return render(request, "login.html", {"form": form})


def signup_view(request):
    """Handles signup form POST data"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            login(request, user)
            return redirect("/main/")
      
        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
        return redirect("/signup/")
 

    form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})


def logout_view(request):
    """Logs user out"""
    logout(request)
    return redirect("/")


@login_required
def send_sniff_request(request, user_ID):
    """Creates new sniff request in DB"""
    from_user = request.user
    to_user = DawgHouseUser.objects.get(id=user_ID)
    sniff_request, created = SniffRequest.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        messages.success(request, "Sniff request sent successfully.")
        return redirect("profile", username=to_user.username)

    messages.warning(request, "Sniff request was already sent.")
    return redirect("profile", username=to_user.username)


@login_required
def accept_sniff_request(request, request_ID):
    """Moves sniff request to friends table and deltes from sniff table"""
    sniff_request = SniffRequest.objects.get(id=request_ID)
    if sniff_request.to_user == request.user:
        sniff_request.to_user.friends.add(sniff_request.from_user)
        sniff_request.from_user.friends.add(sniff_request.to_user)
        sniff_request.delete()
        return redirect("home_view")

    return redirect("home_view")

@login_required
def decline_sniff_request(request, request_id):
    """Deletes sniff from table"""
    sniff_request = SniffRequest.objects.get(id=request_id)
    if sniff_request.to_user == request.user:
        sniff_request.delete()
        return redirect("home_view")
 
    return redirect("home_view")

@login_required
def send_example_view(request):
    """Sends information to DB to make new sniff request"""
    allusers = DawgHouseUser.objects.all()
    all_sniff_requests = SniffRequest.objects.all()

    context = {
        "allusers": allusers,
        "all_sniff_requests": all_sniff_requests,
    }
    return render(request, "sniff_example.html", context)


@login_required
def accept_example_view(request):
    """Renders sniff request template"""
    all_sniff_requests = SniffRequest.objects.all()

    context = {
        "all_sniff_requests": all_sniff_requests,
    }
    return render(request, "accept_sniffs_example.html", context)


def profile_view(request, username):
    """Determines which profile template to render and renders it"""
    logged_in_user = request.user
    user = get_object_or_404(DawgHouseUser, username=username)
    friends_list = user.friends.all()
    barks = Bark.objects.filter(user=user).order_by("-timestamp")
    context = {
    "user": user,
    "barks": barks,
    "friends_list": friends_list,
    "logged_in_user": logged_in_user
    }
    if user == request.user:
        return render(request, "user_profile.html", context)
    if request.user in user.friends.all():
        return render(request, "friend_view.html", context)

    return render(request, "non_friend_view.html", context)


@login_required
def post_bark(request):
    """Logic for posting a new bark"""
    if request.method == "POST":
        bark_content = request.POST.get("bark_content")

        new_bark = Bark(user=request.user, content=bark_content)
        new_bark.save()

        return redirect(f"/profile/{request.user.username}/")

    return redirect("/")

@login_required
def home_post_bark(request):
    """Logic for posting a bark from homepage"""
    if request.method == "POST":
        bark_content = request.POST.get("bark_content")

        new_bark = Bark(user=request.user, content=bark_content)
        new_bark.save()

        return redirect("/main/")

    return redirect("/")

@login_required
def delete_bark(request, id):
    """Logic for deleting a bark"""
    post = get_object_or_404(Bark, pk=id)

    if request.method == "DELETE":
        # Check if the user has permission to delete the post
        if request.user == post.user:
            post.delete()  # Delete the post
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Permission denied"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@csrf_exempt
@login_required
def repost_post(request, bark_id):
    """Logic for reposting"""
    if request.method == "POST":
        # Get the original bark
        original_bark = get_object_or_404(Bark, id=bark_id)
        existing_repost = Bark.objects.filter(
            original_bark=original_bark,
            user=request.user,
            is_repost=True
        ).first()

        if existing_repost:
            existing_repost.delete()
            original_bark.num_howls -= 1
            original_bark.save()
            return JsonResponse({"success": True, "is_repost": False})
        # Create a new Bark instance
        new_bark = Bark(
            content=original_bark.content,
            user=request.user,  # Use the currently logged-in user as the author
            is_repost=True,
            original_bark=original_bark,
        )
        original_bark.num_howls += 1
        new_bark.save()
        original_bark.save()

        return JsonResponse({"success": True, "is_repost":True})
    return JsonResponse({"success": False})


@csrf_exempt
@login_required
def edit_bark_ajax(request):
    """Ajax logic for editing a post"""
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        new_content = data.get("new_content")
        post = Bark.objects.filter(id=post_id).first()

        if (
            post and request.user == post.user
        ):  # Check if the post exists and the user is the owner of the bark
            post.content = new_content
            post.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@login_required
def add_comment(request, bark_id):  # include bark_id here
    """Logic for adding a comment to a post"""
    if request.method == "POST":
        comment_text = request.POST.get("comment_text")
        user = request.user

        if comment_text:
            bark = Bark.objects.get(id=bark_id)  # now bark_id is defined
            comment = Comment(bark=bark, name=user, body=comment_text)
            bark.num_yips = Comment.objects.filter(bark=bark).count() + 1
            comment.save()
            bark.save()

            return JsonResponse({"user": user.username, "text": comment_text})

        return JsonResponse({"error": "Comment text is empty"}, status=400)

    return JsonResponse({}, status=400)


@login_required
def delete_comment(request, comment_id):
    """Logic for deleting a comment"""
    try:
        comment = Comment.objects.get(id=comment_id)

        # Check if the user is the owner of the comment or the owner of the Bark.
        if request.user in (comment.name, comment.bark.user):
            comment.delete()

            bark = comment.bark
            bark.num_yips = Comment.objects.filter(bark=bark).count()
            bark.save()

            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Permission denied"})
    except Comment.DoesNotExist:
        return JsonResponse({"success": False, "error": "Comment not found"})


@login_required
def give_treat(request, bark_id, user_which, return_to):
    """Logic for liking a post"""
    bark = get_object_or_404(Bark, id=bark_id)
    user = request.user

    if user in bark.treated_by.all():
        bark.num_likes -= 1
        bark.treated_by.remove(user)
    else:
        bark.num_likes += 1
        bark.treated_by.add(user)

    bark.save()

    if return_to == "main_timeline":
        return redirect("main_timeline")
    if return_to == "profile":
        return redirect(f"/profile/{user_which}/")
  
    return redirect(f"/profile/{return_to}/")


@method_decorator(csrf_exempt, name="dispatch")
def edit_bio_ajax(request):
    """Ajax logic for editing a bio"""
    if request.method == "POST":
        data = json.loads(request.body)
        new_bio = data.get("bio")
        request.user.bio = new_bio
        request.user.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def search_users(request):
    """Fuzzy username matching alogorithm"""
    if request.method == "POST":
        username = request.POST.get("username", None)
        if username:
            users = DawgHouseUser.objects.all()
            similar_users = []
            for user in users:
                dist = distance(username, user.username)
                username_length = len(username)
                similarity_ratio = (
                    1 - dist / max(username_length, len(user.username))
                ) * 100
                if similarity_ratio >= 60:
                    similar_users.append(user)
            return render(
                request, "search_results.html", {"similar_users": similar_users}
            )
    return render(request, "search_users.html")


@login_required
def main_timeline(request):
    """Retrieves all posts to display and renders homepage template"""
    user = request.user
    friends = user.friends.all()
    barks = Bark.objects.filter(Q(user=user) | Q(user__in=friends)).order_by(
        "-timestamp"
    )

    for friend in friends:
        print(friend.username)

    context = {
        "barks": barks,
    }
    return render(request, "main_page.html", context)

@login_required
def change_profile_picture(request, picture_path):
    """Sets 'profile_picture' in DB to static image path"""
    request.user.profile_picture = picture_path
    request.user.save()
    
    return redirect(f"/profile/{request.user.username}")
