"""Middleware module."""
from purapps.purbeurre.forms import SearchProduct
from django.shortcuts import redirect


class SearchMiddleware:
    """SearchMiddleware class."""

    def __init__(self, get_response):
        """Init."""
        self.get_response = get_response

    def __call__(self, request):
        """Call."""
        search_form = SearchProduct()

        if request.method == "POST" and request.POST.get("product_name"):
            product_name = request.POST.get("product_name")
            return redirect("results", product_name=product_name)

        request.search_form = search_form
        return self.get_response(request)
