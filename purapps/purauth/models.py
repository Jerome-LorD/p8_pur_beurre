"""Purauth models module."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# User = get_user_model()


class User(AbstractUser):
    """Custom user."""

    # nickname = models.CharField("Nom d'utilisateur", max_length=100, unique=True)
    # is_active = models.BooleanField(default=True)

    # USERNAME_FIELD = "nickname"
    # REQUIRED_FIELDS = ("password",)
    # pass
