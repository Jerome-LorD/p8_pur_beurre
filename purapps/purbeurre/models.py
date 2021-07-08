"""Models module."""

from django.db import models
from django.db.models import Subquery, Value, Count, F
from django.contrib.postgres.aggregates import StringAgg


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

    name = models.CharField(max_length=150, unique=True, default=False, blank=True)
    brand = models.CharField(max_length=150, default=False, blank=True)
    stores = models.CharField(max_length=150, default=False, blank=True)
    image = models.URLField(max_length=255, default=False, blank=True, null=True)
    url = models.CharField(max_length=255, unique=True, default=False, blank=True)
    categories = models.ManyToManyField(Category, related_name="category_owner")
    nutriscore = models.ForeignKey(Nutriscore, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.name} - {self.brand} - {self.stores} - {self.url}\
 - {self.nutriscore} - {self.image}"

    @classmethod
    def get_substitute(cls, category_id):
        """Get the substitute."""
        result = (
            Product.objects.filter(categories=category_id)
            .order_by("nutriscore__type")
            .first()  # ,
            # nutriscore__type__lt=Subquery(
            #         Product.objects.annotate(fake_group_by=Value(1))
            #         .values("fake_group_by")
            #         .annotate(
            #             liste=StringAgg(
            #                 "nutriscore__type", delimiter=", ", distinct=True
            #             )
            #         )
            #         .values("liste")
            #         .filter(categories=category_id)
            #     ),
            # ).values("name", "nutriscore__type", "image")
            # # .order_by("nutriscore__type")
            # .order_by("?")[:1]
        )
        # breakpoint()
        return (
            result
            if result
            else {"name": "pas de meilleur nutriscore pour ce produit."}
        )


class Substitutes(models.Model):
    """Create substitutes table."""

    substitute = models.ForeignKey(
        Product, related_name="substitute", blank=True, on_delete=models.CASCADE
    )
    substituted = models.ForeignKey(
        Product, related_name="substituted", blank=True, on_delete=models.CASCADE
    )
