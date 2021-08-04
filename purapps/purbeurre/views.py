"""Purbeurre views module."""

import json
from django.http.response import Http404
from django.shortcuts import render, HttpResponse, redirect
from purapps.purbeurre.forms import SearchProduct
from purapps.purbeurre.models import Product, Substitutes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):
    """Index."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)
    else:
        search_form = SearchProduct()

    context = {"search_form": search_form}
    return render(request, "pages/home.html", context and locals())


def results(request, product_name):
    """Results."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)

    search_form = SearchProduct()
    result = Product.objects.filter(name__iregex=r"^%s$" % product_name)
    if result:

        origin_prod_name = result[0].name
        origin_nutriscore = result[0].nutriscore.type.capitalize()
        origin_category = result[0].categories.values("id")
        origin_image = result[0].image

        substit = Product.find_substitute(result[0].id)
        page = request.GET.get("page", 1)
        paginator = Paginator(substit, 8)
        try:
            page_result = paginator.page(page)
        except PageNotAnInteger:
            page_result = paginator.page(1)
        except EmptyPage:
            page_result = paginator.page(paginator.num_pages)

        return render(
            request,
            "pages/results.html",
            {
                "search_form": search_form,
                "substit": substit,
                "origin_prod_name": origin_prod_name,
                "origin_image": origin_image,
                "origin_nutriscore": origin_nutriscore,
                "page_result": page_result,
            },
        )
    else:
        no_result = Product.objects.filter(name__icontains="%s" % product_name)
        page_no_res = request.GET.get("page", 1)
        paginator = Paginator(no_result, 8)
        try:
            page_no_result = paginator.page(page_no_res)
        except PageNotAnInteger:
            page_no_result = paginator.page(1)
        except EmptyPage:
            page_no_result = paginator.page(paginator.num_pages)
        search_form = SearchProduct()
        return render(
            request,
            "pages/results.html",
            {
                "search_form": search_form,
                "search_term": product_name,
                "page_no_result": page_no_result,
                "no_result": no_result,
            },
        )


def err_404(request, exception=None):
    """Error 404 view."""
    return render(request, "pages/404.html")


def product_details(request, product_name):
    """Product details."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)

    search_form = SearchProduct()
    try:
        product = Product.objects.get(name=product_name)
        fat = product.nutriments["fat_100g"]
        salt = product.nutriments["salt_100g"]
        sodium = product.nutriments["sodium_100g"]
        energy = product.nutriments["energy_100g"]
        energy_kcal = product.nutriments["energy-kcal_100g"]
        sugars = product.nutriments["sugars_100g"]
        proteins = product.nutriments["proteins_100g"]
        carbohydrates = product.nutriments["carbohydrates_100g"]
    except Product.DoesNotExist:
        raise Http404("Cette page n'existe pas")
    return render(
        request,
        "pages/product.html",
        {
            "product": product,
            "fat": fat,
            "salt": salt,
            "sodium": sodium,
            "energy": energy,
            "energy_kcal": energy_kcal,
            "sugars": sugars,
            "proteins": proteins,
            "carbohydrates": carbohydrates,
            "search_form": search_form,
        },
    )


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


@csrf_exempt
def ajax(request):
    """Ajax post method."""
    if request.is_ajax():
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        products = body["products"]
        user_id = body["user_id"]
        origin_product = body["origin_product"]

        origin_product = origin_product.replace("&amp;", "&")
        origin_product = Product.objects.get(name=origin_product)

        for item_id in products:
            if Substitutes.objects.filter(
                product_id=item_id,
                reference_id=origin_product.id,
                user_id=int(user_id),
            ).exists():
                pass

            else:
                substitute = Substitutes(
                    product_id=item_id,
                    reference_id=origin_product.id,
                    user_id=int(user_id),
                )
                substitute.save()

        return render(request, "pages/product.html", {"products": products})


@login_required
def favorites(request):
    """Retrieve favorites."""
    if request.method == "POST":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)

    search_form = SearchProduct()

    res = Substitutes.objects.filter(user=request.user)

    search_form = SearchProduct()

    return render(
        request,
        "pages/favorites.html",
        {"products": res, "search_form": search_form},
    )
