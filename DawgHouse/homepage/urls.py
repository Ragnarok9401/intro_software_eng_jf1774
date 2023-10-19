from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", views.logout_view, name="logout_view"),
    path("send_sniff_request/<int:user_ID>/", views.send_sniff_request, name="send_sniff_request"),
    path('accept_sniff_request/<int:request_ID>/', views.accept_sniff_request, name='accept_sniff_request'),
    path("accept_example/", views.accept_example_view, name="accept_example"),
    path("send_example/", views.send_example_view, name="send_example"),
    path("profile/<str:username>/", views.ProfileView, name='profile'),
    path("edit/<str:username>/", views.userEdit, name="edit_profile"),
]
