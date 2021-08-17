"""Purauth urls module."""
from django.urls import path
from purapps.purauth import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("accounts/inscript/", views.inscript, name="inscript"),
    path(
        "accounts/login/",
        views.login,
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logout.html", next_page="/"
        ),
        name="user_logout",
    ),
    path("accounts/profile/", views.user_profile, name="profile"),
]
