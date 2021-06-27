"""Models module."""

from django.db import models
from django.db.models.deletion import CASCADE

# from django.contrib import admin

# Create your models here.


class Nutriscore(models.Model):
    """Create nutriscore table."""

    type = models.CharField(max_length=1, unique=True)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.type}"


class Category(models.Model):
    """Create category table."""

    name = models.CharField(max_length=120, unique=True, default=False)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.name}"


class Product(models.Model):
    """Create product table."""

    name = models.CharField(max_length=150, unique=True, default=False, blank=True)
    brand = models.CharField(max_length=150, default=False, blank=True)
    stores = models.CharField(max_length=150, default=False, blank=True)
    url = models.CharField(max_length=255, unique=True, default=False, blank=True)
    categories = models.ManyToManyField(Category, related_name="categories", blank=True)
    nutriscore = models.ForeignKey(Nutriscore, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.name} - {self.brand} - {self.stores} - {self.url}"


class Substitutes(models.Model):
    """Create substitutes table."""

    substitute = models.ForeignKey(
        Product, related_name="substitute", blank=True, on_delete=models.CASCADE
    )
    substituted = models.ForeignKey(
        Product, related_name="substituted", blank=True, on_delete=models.CASCADE
    )


# class CreateDbAdmin(admin.ModelAdmin):
