"""Purauth admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User
from .forms import UserCreationForm

admin.site.register(User)


class UserAdmin(AuthUserAdmin):
    """User admin class."""

    add_form = UserCreationForm

    model = User
