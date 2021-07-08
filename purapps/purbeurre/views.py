"""Purbeurre views module."""

import json
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from purapps.purbeurre.forms import SearchProduct
from purapps.purbeurre.models import Product


def index(request):
    """Index."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")
            result = (
                Product.objects.filter(name__iregex=r"^%s$" % product_name)
                .values("name", "image", "categories", "nutriscore__type")
                .order_by("-categories")[:1]
            )
            # breakpoint()
            if result:
                category_id = result[0].get("categories")

                substit = Product.get_substitute(category_id)
                substitute = substit.name  # .get("name")
                substriscore = substit.nutriscore.type  # .get("nutriscore__type")
                image = substit.image  # get("image")

    else:
        search_form = SearchProduct()

    context = {"search_form": search_form}
    return render(request, "pages/home.html", context and locals())


class HomeView(TemplateView):
    """HomeView class."""

    template_name = "home.html"


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
