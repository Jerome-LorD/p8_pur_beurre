"""Purbeurre views module."""

import json
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from purapps.purbeurre.models import Product, Substitutes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):
    """Index."""
    return render(request, "pages/home.html")


def mentions(request):
    """Mentions."""
    return render(request, "pages/mentions.html")


def results(request, product_name):
    """Results view from search product form."""
    try:
        result = Product.objects.filter(name__iregex=r"^%s$" % product_name)
    except Product.DoesNotExist:
        raise Http404("Cette page n'existe pas")

    page = request.GET.get("page", 1)
    if result.first():
        product = result.first()
        substit = product.find_substitute()
        if substit is not None:
            paginator = Paginator(substit, 16)
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
                    "substit": substit,
                    "product": product,
                    "page_result": page_result,
                },
            )

        else:
            no_result = "Il n'y a pas de substitut pour ce produit."
            return render(
                request,
                "pages/results.html",
                {
                    "product": product,
                    "no_result": no_result,
                },
            )

    elif not result.first():

        general_research = Product.objects.filter(
            name__icontains="%s" % product_name
        ).order_by("nutriscore__type")

        gal_search = general_research.all()
        paginator = Paginator(gal_search, 16)

        try:
            page_no_result = paginator.page(page)
        except PageNotAnInteger:
            page_no_result = paginator.page(1)
        except EmptyPage:
            page_no_result = paginator.page(paginator.num_pages)

        return render(
            request,
            "pages/results.html",
            {
                "gal_search": gal_search,
                "search_term": product_name,
                "page_no_result": page_no_result,
            },
        )

    return render(request, "pages/results.html", {"search_term": product_name})


def error_404(request, exception):
    """Error 404 view."""
    return render(request, "pages/404.html", status=404)


def product_details(request, product_name):
    """Product details."""
    try:
        product = Product.objects.get(name=product_name)
    except Product.DoesNotExist:
        raise Http404("Cette page n'existe pas")
    return render(
        request,
        "pages/product.html",
        {
            "product": product,
        },
    )


def autocomplete(request):
    """Jquery autocomplete response."""
    if request.is_ajax() and request.method == "GET":
        product = request.GET.get("term", "")
        products = Product.objects.filter(name__icontains="%s" % product).order_by(
            "id"
        )[:10]

    return JsonResponse([{"name": item.name} for item in products], safe=False)


@csrf_exempt
def save_substitutes(request):
    """Save substitutes from ajax post."""
    if request.is_ajax():
        data = json.loads(request.body)
        products = data["products"]
        ref_product_id = data["ref_product_id"]
        ref_product = Product.objects.get(pk=ref_product_id)

        for item_id in products:

            Substitutes.objects.get_or_create(
                product_id=item_id, reference_id=ref_product.id, user_id=request.user.id
            )

    return render(request, "pages/results.html", {"products": products})


@login_required
def favorites(request):
    """Retrieve favorites."""
    products = Substitutes.objects.filter(user=request.user)

    return render(
        request,
        "pages/favorites.html",
        {"products": products},
    )
