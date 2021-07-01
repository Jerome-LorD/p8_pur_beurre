"""Purbeurre views module."""

import json
from django.http.response import JsonResponse

# from django.http.response import HttpResponse

from django.shortcuts import render, redirect, HttpResponse  # , render_to_response

# from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from purapps.purbeurre.forms import SearchProduct

# from purapps.purauth.forms import NewLoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

from purapps.purbeurre.models import Product

# from purapps.purbeurre.models import Product, Substitutes, Category, Nutriscore
from purapps.purbeurre.utils import Downloader, OffCleaner, Insert

# from django.contrib.auth.decorators import login_required

# from purbeurre.utils import Downloader, OffCleaner, Insert

# from forms import SearchProduct


def index(request):
    """Index."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")
            result = Product.objects.filter(name__icontains=product_name).values("name")
    else:
        search_form = SearchProduct()

    context = {"search_form": search_form}
    return render(request, "pages/home.html", context and locals())


class HomeView(TemplateView):
    """HomeView class."""

    template_name = "home.html"


# def inscript(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect("/home")
#     else:
#         form = UserCreationForm()
#     return render(request, "pages/inscript.html", {"form_ins": form})


def autocomplete(request):
    """Jquery autocomplete response."""
    if request.is_ajax() and request.method == "GET":
        product = request.GET.get("term", "")
        products = Product.objects.filter(name__icontains="%s" % product).order_by(
            "id"
        )[:7]

        data = json.dumps([{"name": item.name} for item in products])
    else:
        data = "Le chargement n'a pas pu se faire."
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
