"""Tests purbeurre models module."""
from purapps.purbeurre.models import Category, Product, Nutriscore
from django.test import TestCase


class FindSubstitutesTestCase(TestCase):
    """FindSubstitutesTestCase class."""

    def setUp(self):
        """Make Setup."""
        data = {
            "products": [
                {
                    "product_name_fr": "Chocolat bio",
                    "brands": "Cote d'Or",
                    "image_small_url": "http://www.chocolat-bio",
                    "nutriments": {"bli_100g": "bli"},
                    "url": "http A",
                    "nutriscore_grade": "d",
                    "categories": "Chocolat, Tablette de chocolat, Tablette de chocolat noir",
                },
                {
                    "product_name_fr": "Chocolat noir sans sucres",
                    "brands": "Gerblé",
                    "image_small_url": "http image B",
                    "nutriments": {"blo_100g": "blo"},
                    "url": "http B",
                    "nutriscore_grade": "c",
                    "categories": (
                        "Chocolat, Tablette de chocolat, Tablette de chocolat noir,\
                             Tablette de chocolat noir sans suvres"
                    ),
                },
                {
                    "product_name_fr": "Milka choco Moooo",
                    "brands": "Milka",
                    "image_small_url": "http image C",
                    "nutriments": {"blu_100g": "blu"},
                    "url": "http C",
                    "nutriscore_grade": "e",
                    "categories": (
                        "Biscuit, Biscuit au chocolat, Biscuit au chocolat\
                         au lait"
                    ),
                },
            ]
        }

        for product in data["products"]:

            try:
                Nutriscore.objects.get(type=product["nutriscore_grade"])
            except Nutriscore.DoesNotExist:
                Nutriscore.objects.create(type=product["nutriscore_grade"])

            try:
                Product.objects.get(name=product["product_name_fr"])
            except Product.DoesNotExist:

                last_nut = Nutriscore.objects.filter(
                    type=product["nutriscore_grade"]
                ).values("id")

                Product.objects.create(
                    name=product["product_name_fr"],
                    url=product["url"],
                    brand=product["brands"],
                    nutriments={
                        f"{k}": v
                        for k, v in product["nutriments"].items()
                        if "100g" in k
                    },
                    image=product["image_small_url"],
                    nutriscore_id=last_nut,
                )

                for category in product["categories"].split(","):
                    categorie = category.strip()

                    try:
                        Category.objects.get(name=categorie)
                    except Category.DoesNotExist:

                        Category.objects.create(name=categorie)

                    prod = Product.objects.get(name=product["product_name_fr"])

                    category = Category.objects.filter(name=categorie).values("id")[0]

                    prod.categories.add(category.get("id"))

                    result = Product.objects.filter(
                        name__iregex=r"^%s$" % "Chocolat bio"
                    )
                    self.product = result.first()

    def test_find_substitute(self):
        """Test find substitutes."""
        substit = self.product.find_substitute()
        if substit is not None:
            substit = substit.first()
            self.assertEqual(substit.name, "Chocolat noir sans sucres")
