from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", views.logout_view, name="logout_view")
]
