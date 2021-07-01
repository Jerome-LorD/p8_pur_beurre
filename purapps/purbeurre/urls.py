"""Urls app module."""
import debug_toolbar

from django.urls import path, include
from django.views.generic import TemplateView

from . import views

# from purapps import purbeurre
# from django.contrib.auth import views as auth_views

# app_name = purbeurre

urlpatterns = [
    path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="index"),
    path("autocomplete/", views.autocomplete),
    path("__debug__/", include(debug_toolbar.urls)),
]
