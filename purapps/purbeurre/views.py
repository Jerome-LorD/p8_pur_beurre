"""Purbeurre views module."""
# from django.http.response import HttpResponse

from django.shortcuts import render, redirect  # , render_to_response

# from django.http import HttpResponse
from django.views.generic import TemplateView  # , FormView
from purapps.purbeurre.forms import SearchProduct
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# from purbeurre.utils import Downloader, OffCleaner, Insert

# from forms import SearchProduct


def index(request):
    """Index."""
    if request.method == "GET":
        search_form = SearchProduct(request.POST or None)
        if search_form.is_valid():
            search_form = SearchProduct()
            # vid = request.GET.get("vid")
    else:
        search_form = SearchProduct()

    context = {"search_form": search_form}
    return render(request, "pages/home.html", context and locals())


class HomeView(TemplateView):
    """HomeView class."""

    template_name = "home.html"


def inscript(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/home")
    else:
        form = UserCreationForm()
    return render(request, "pages/inscript.html", {"form_ins": form})


@login_required
def user_profile(request):
    """Account."""
    first_name = request.user.first_name
    context = {"first_name": first_name}
    return render(request, "registration/profile.html", context)


# class SearchView(FormView):
#     template_name = "home.html"
#     form_class = SearchProduct

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super().form_valid(form)

# def get_context_data(self, **kwargs):
#     context = super(SearchView, self).get_context_data(**kwargs)
#     # This method is called when valid form data has been POSTed.
#     # It should return an HttpResponse.
#     context = {"form_class": self.form_class}
#     # print(context)
#     return context
