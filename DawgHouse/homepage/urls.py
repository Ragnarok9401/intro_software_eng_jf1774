from django.urls import path
from . import views
from .views import ProfileView

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<str:username>/", views.ProfileView, name="profile"),
]
