"""Models module."""

from django.db import models
from django.db.models.deletion import CASCADE

# from django.contrib import admin

# from django.conf import settings

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
    categories = models.ManyToManyField(Category, related_name="category_owner")
    nutriscore = models.ForeignKey(Nutriscore, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return str representation."""
        return f"{self.id} - {self.name} - {self.brand} - {self.stores} - {self.url}\
 - {self.nutriscore}"

    def get_substitute(self):
        """Get the substitute."""


class Substitutes(models.Model):
    """Create substitutes table."""

    substitute = models.ForeignKey(
        Product, related_name="substitute", blank=True, on_delete=models.CASCADE
    )
    substituted = models.ForeignKey(
        Product, related_name="substituted", blank=True, on_delete=models.CASCADE
    )


# select p.name, c.name
# from products p
# join categories_products cp
# on cp.products_id = p.id
# join categories c
# on cp.categories_id = c.id
# where p.id = 10
# order by c.id desc limit 1;

# Product.objects.filter(categories__category_owner__id=10).values("name","categories__name").order_by("-categories")[:1]

# récupération de la catégorie. L'id est suffisant :
# Product.objects.filter(categories__category_owner__id=10).values("name","categories").order_by("-categories")[:1]
# il faut rechercher les produits
# de cette catégorie dont le nutriscore est mieux que celui du pdt recherché.


# select p.name product, n.type nutriscore, c.name category
# from purbeurre_product p
# join purbeurre_product_categories cp
# on cp.product_id = p.id
# join purbeurre_category c
# on cp.category_id = c.id
# join purbeurre_nutriscore n
# on n.id = p.nutriscore_id
# where c.id = 5 and n.type < "e";
# -- order by c.id desc limit 1;
