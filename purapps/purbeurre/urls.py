"""Urls app module."""
import debug_toolbar

from django.urls import path, include
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="index"),
    path("results/<str:product_name>", views.results, name="results"),
    path("autocomplete/", views.autocomplete),
    path("results/autocomplete/", views.autocomplete),
    path("__debug__/", include(debug_toolbar.urls)),
]
