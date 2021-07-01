"""Purauth module."""
# from purapps.purauth.forms import LoginForm
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.messages import constants as messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from .forms import InscriptForm, NewLoginForm

# Create your views here.
# def signup(request):
#     return render(request, "signup.html")


# def user_login(request):
#     """Authenticate a user."""
#     # Etape 1 :
#     email = request.POST["email"]  # <- changement
#     password = request.POST["password"]

#     # Etape 2 :
#     user = authenticate(request, email=email, password=password)  # <- changement

#     # Etape 3 :
#     if user is not None:
#         login(request, user)
#         messages.add_message(request, messages.SUCCESS, "Vous êtes connecté !")
#     else:
#         messages.add_message(
#             request, messages.ERROR, "Les champs renseignés sont invalides."
#         )

#     return redirect("home")


# Create your views here.
# def inscriptions(request):
#     return render(request, "inscriptions/")


# def inscript(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect("/")
#     else:
#         form = UserCreationForm()
#     return render(request, "registration/inscript.html", {"form_ins": form})


def inscript(request):
    if request.method == "POST":
        form = InscriptForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/")
    else:
        form = InscriptForm()
    return render(request, "registration/inscript.html", {"form_ins": form})


# class LoginView(TemplateView):

#     template_name = "registration/login.html"
#     form_class = LoginForm

#     def post(self, request, *args, **kwargs):
#         username = request.POST["username"]
#         password = request.POST["password"]
#         form = self.form_class(request.POST)
#         user = authenticate(username=username, password=password)

#         if user is not None and user.is_active:
#             auth_login(request, user)
#             # return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )
#             return HttpResponseRedirect("/")

#         return render(request, self.template_name, {"form": form})


def login(request):
    form = NewLoginForm(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        request, messages.SUCCESS, "Vous êtes connecté !"
        return redirect("/accounts/profile")
    else:
        request, messages.ERROR, "Les champs renseignés sont invalides."
        form = NewLoginForm()
    return render(request, "registration/login.html", {"form": form})


# def loginView(request):
#     form = LoginForm(request.POST)
#     return render(request, "registration/login.html", {"form_log": form})


@login_required
def user_profile(request):
    """Account."""
    first_name = request.user.first_name
    context = {"first_name": first_name}
    return render(request, "registration/profile.html", context)
