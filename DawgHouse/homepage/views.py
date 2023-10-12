from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User

from .models import Bark, User, Relationship, Profile


def home(request):
    return render(request, "index.html")

#def profile(request):
#    return HttpResponse("Profile")  #example to show profile page works

def ProfileView(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    followers = Relationship.objects.filter(to_user=user)
    following = user_profile.follows.all()
    posts = Bark.objects.filter(user=username)
    context = {'user': user, 'user_profile' : user_profile, 'posts': posts, 'followers' : followers, 'following' : following}
    return render(request, 'user_profile.html', context)

