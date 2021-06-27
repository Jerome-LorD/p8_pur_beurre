from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

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


def inscript(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "pages/inscript.html", {"form_ins": form})
