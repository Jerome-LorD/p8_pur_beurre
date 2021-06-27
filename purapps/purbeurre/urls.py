"""Urls app module."""
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

# from purapps import purbeurre
from django.contrib.auth import views as auth_views

# app_name = purbeurre

urlpatterns = [
    path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="index"),
    path(
        "account/inscript/",
        auth_views.LoginView.as_view(template_name="registration/inscript.html"),
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logout.html", next_page="/"
        ),
    ),
    path("accounts/profile/", views.user_profile, name="profile"),
]
