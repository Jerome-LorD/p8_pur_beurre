"""Purbeurre views module."""

import json
import re
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from purapps.purbeurre.forms import SearchProduct
from purapps.purbeurre.models import Product, Substitutes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect, csrf_exempt


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


def product_details(request):
    """Product details."""
    product = Product.retrieve_substitute()
    return render(request, "pages/product.html", {"product": product})


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
        print(products, origin_product)

        origin_product = Product.objects.get(name=origin_product)

        for i in products:
            if Substitutes.objects.filter(
                product_id=i,
                reference_id=origin_product.id,
                user_id=int(user_id),
            ).exists():
                pass

            else:
                t = Substitutes(
                    product_id=i,
                    reference_id=origin_product.id,
                    user_id=int(user_id),
                )
                t.save()

        return render(request, "pages/product.html", {"products": products})


def favorites(request):
    """Retrieve favorites."""
    res = Substitutes.objects.values(
        "product__name",
        "product__image",
        "reference__name",
        "reference__image",
        "product__nutriscore__type",
        "user_id",
    )
    search_form = SearchProduct()

    return render(
        request, "pages/favorites.html", {"products": res, "search_form": search_form}
    )
