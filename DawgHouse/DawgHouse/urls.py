"""
URL configuration for DawgHouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("signup/", include("homepage.urls")),
    path("login/", include("homepage.urls")),
    path("accept_example/", include("homepage.urls")),
    path("send_example/", include("homepage.urls")),
    path("send_sniff_request/<int:user_ID>/", include("homepage.urls")),
    path("accept_sniff_request/<int:request_ID>", include("homepage.urls")),
    path("profile/<str:username>/", include("homepage.urls")),
    path("edit/<str:username>/", include("homepage.urls")),
    path("search/", include("homepage.urls")),
]
