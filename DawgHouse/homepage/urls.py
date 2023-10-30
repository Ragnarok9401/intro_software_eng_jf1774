from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", views.logout_view, name="logout_view"),
    path(
        "send_sniff_request/<int:user_ID>/",
        views.send_sniff_request,
        name="send_sniff_request",
    ),
    path(
        "accept_sniff_request/<int:request_ID>/",
        views.accept_sniff_request,
        name="accept_sniff_request",
    ),
    path("accept_example/", views.accept_example_view, name="accept_example"),
    path("send_example/", views.send_example_view, name="send_example"),
    path("profile/<str:username>/", views.ProfileView, name="profile"),
    path("post_bark/", views.post_bark, name="post_bark"),
    path('give_treat/<uuid:bark_id>/<str:user_which>/', views.give_treat, name='give_treat'),
    path("edit_bio/", views.edit_bio_ajax, name="edit_bio_ajax"),
    path('search_users/', views.search_users, name='search_users'),
    path('main/', views.main_timeline, name="main_timeline"),
    path('add_comment/<str:bark_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('bark_edit/', views.edit_bark_ajax, name='edit_bark_ajax'),
    path('delete_bark/<uuid:id>/', views.delete_bark, name='delete_bark'),
    path('repost/<uuid:bark_id>/', views.repost_bark, name='repost_bark'),
]
