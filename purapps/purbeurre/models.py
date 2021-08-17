"""Models module."""

from django.db import models
from django.db.models import Count
from django.conf import settings
from django.urls import reverse


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

    @classmethod
    def find_best_category(cls):
        """Find the best category."""


class Product(models.Model):
    """Create product table."""

    name = models.CharField(max_length=250, unique=True, default=False, blank=True)
    brand = models.CharField(max_length=180, default=False, blank=True)
    image = models.URLField(max_length=255, default=False, blank=True, null=True)
    nutriments = models.JSONField()
    url = models.CharField(max_length=255, unique=True, default=False, blank=True)
    categories = models.ManyToManyField(Category, related_name="category_owner")
    nutriscore = models.ForeignKey(Nutriscore, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.name} - {self.brand} - {self.url} - {self.nutriscore}\
 - {self.image} - {self.nutriments}"

    @classmethod
    def find_substitute(cls, product_id):
        """Find a substitute."""
        data = Product.objects.filter(id=product_id).order_by("categories")
        categories_id = data[0].categories.values("id").order_by("id")
        sorted_categories = (
            Product.objects.filter(categories__in=categories_id)
            .values("categories__id")
            .annotate(tot=Count("id", distinct=True))
            .order_by("tot")
        )
        if len(sorted_categories) > 1:
            offset = 0
            best_cat = sorted_categories[offset].get("categories__id")
            substitute = Product.objects.filter(
                categories__id=best_cat, nutriscore__type__lt=data[0].nutriscore.type
            )

            while not substitute:
                best_cat = sorted_categories[offset].get("categories__id")
                substitute = Product.objects.filter(
                    categories__id=best_cat,
                    nutriscore__type__lt=data[0].nutriscore.type,
                )

                offset += 1
                if data[0].nutriscore.type > "b":
                    offset_limit = 4
                offset_limit = 3
                if offset == offset_limit and not substitute:
                    substitute = data
            return substitute
        return data


class Substitutes(models.Model):
    """Create substitutes table."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_id",
        default=False,
        blank=True,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product, related_name="product", default="", on_delete=models.CASCADE
    )
    reference = models.ForeignKey(
        Product, related_name="reference", default="", on_delete=models.CASCADE
    )
