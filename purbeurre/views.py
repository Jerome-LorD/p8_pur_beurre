"""Purbeurre views module."""
# from django.http.response import HttpResponse

# from django.shortcuts import render, render_to_response
from django.http import HttpResponse


def index(request):
    """Base index."""
    return HttpResponse("Pur beurre")
