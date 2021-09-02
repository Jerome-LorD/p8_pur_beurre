"""Purauth module."""

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptForm, NewLoginForm


def inscript(request):
    """Inscript view."""
    if request.method == "POST":
        form = InscriptForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/")
    else:
        form = InscriptForm()
    return render(request, "registration/inscript.html", {"form_ins": form})


def login(request):
    """Login view."""
    if request.method == "POST":
        login_form = NewLoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect("profile")
    else:
        login_form = NewLoginForm()
    return render(
        request,
        "registration/login.html",
        {"login_form": login_form},
    )


@login_required
def user_profile(request):
    """Account."""
    first_name = request.user.first_name
    context = {"first_name": first_name}
    return render(request, "registration/profile.html", context)


def user_logout(request):
    """Log out."""
    logout(request)
    return redirect("index")
