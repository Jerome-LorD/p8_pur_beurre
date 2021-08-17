"""Urls app module."""
import debug_toolbar

from django.urls import path, re_path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results/<str:product_name>/", views.results, name="results"),
    # re_path(r"^results/(?P<product_name>\w+)/$", views.results, name="results"),
    path("product/<str:product_name>/", views.product_details, name="product"),
    path("favorites/", views.favorites, name="favorites"),
    re_path(r"^autocomplete/", views.autocomplete, name="autocomplete"),
    path("ajax/", views.save_substitutes, name="save_substitutes"),
]
