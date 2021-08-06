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
    if request.method == "POST":    # le formulaire ne devrait pas se résoudre ici
        search_form = SearchProduct(request.POST or None)  # pas sur que le or None soit necessaire
        if search_form.is_valid():
            search_form = SearchProduct()  # à priori inutile ici
            product_name = request.POST.get("product_name")  # tu devrais pouvoir le récupérer depuis le formulaire directement

            return redirect("results", product_name=product_name)
    else:
        search_form = SearchProduct()

    context = {"search_form": search_form}
    return render(request, "pages/home.html", context and locals())  # pourquoi "and locals()" ?


def results(request, product_name):
    """Results."""  # results de quoi ? ;)
    if request.method == "POST":   # le formulaire ne devrait pas se résoudre ici
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)

    search_form = SearchProduct()  # si tu le créé ici, ne le créé pas plus bas ;)
    
    result = Product.objects.filter(name__iregex=r"^%s$" % product_name)
    if result:
        
        # préfère plutôt:
        product = result.first()
        # puis product.name, produuct.nutriscore, etc.
        
        # préfère aussi nommer tes variables sans abréviation ;)

        origin_prod_name = result[0].name
        origin_nutriscore = result[0].nutriscore.type.capitalize()
        origin_category = result[0].categories.values("id")
        origin_image = result[0].image

        substit = Product.find_substitute(result[0].id)  # avec une méthode d'instance, ce sera "product.find_substitute()" tout simplement
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
                # préfère envoyer directement le produit plutot que ses attributs un à un (plus simple et lisible)
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
 
        search_form = SearchProduct()  # existe déjà
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
    if request.method == "POST":   # le formulaire ne devrait pas se résoudre ici
        search_form = SearchProduct(request.POST or None)  # pourquoi "or None" à chaque fois ?
        if search_form.is_valid():
            search_form = SearchProduct()
            product_name = request.POST.get("product_name")

            return redirect("results", product_name=product_name)

    search_form = SearchProduct()
    # dans l'idéal, appel une méthode du produit pour récupérer tous ces éléments - on est dans de la logique métier ici ;)
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


@csrf_exempt  # tu peux implémenter le csrf avec l'ajax, mais ça demande un peu de documentation (django en parle dans sa doc)
def ajax(request):  # qui fait quoi ?
    """Ajax post method."""  # qui fait quoi ?
    if request.is_ajax():
        body_unicode = request.body.decode("utf-8")  # ne décode pas le body comme ça pour récupérer le json, mais utilise seulement la lib json
        # peut être mettre le content-type dans fectch (application/json) pour éviter ce genre de traitement ;) je te laisse te renseigner.
        body = json.loads(body_unicode)
        products = body["products"]
        user_id = body["user_id"]  # pas besoin de passer le user_id puisque tu l'as avec request ;)
        origin_product = body["origin_product"]  # préfère "product" ou "base_product", plus simple. Si tu n'as que le produit et ses substituts, alors "product" et "substitutes" suffit.

        origin_product = origin_product.replace("&amp;", "&") # pas besoin de ça normalement
        origin_product = Product.objects.get(name=origin_product)

        # je ne comprend pas cette partie
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
    if request.method == "POST":  # le formulaire ne devrait pas se résoudre ici
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
