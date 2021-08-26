"""Tests purbeurre models module."""

import unittest
from purapps.purbeurre.models import Category, Product, Nutriscore, Substitutes
from django.test import TestCase, RequestFactory, SimpleTestCase
from purapps.purbeurre.views import favorites, product_details

# from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model

User = get_user_model()


class FillDbTestCase(unittest.TestCase):
    """FindSubstitutesTestCase class."""

    @classmethod
    def setUpClass(cls):
        """Make Setup."""
        if cls is not FillDbTestCase and cls.setUp is not FillDbTestCase.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                FillDbTestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        products = [
            {
                "product_name_fr": "Chocolat bio",
                "brands": "Cote d'Or",
                "image_small_url": "http://www.chocolat-bio",
                "nutriments": {"bli_100g": "bli"},
                "url": "http A",
                "nutriscore_grade": "d",
                "categories": (
                    "Chocolat, Tablette de chocolat,\
                     Tablette de chocolat noir"
                ),
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

        for product in products:

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


class FindSubstitutesTestCase(FillDbTestCase):
    """FindSubstitutesTestCase class."""

    def test_find_substitute_for_Chocolat_bio(self):
        """Test find substitute for chocolat bio.

        With nutriscore D, the substitute must be better and belong to the same
        category or the less distant than the desired product.
        So, the substitute is "Chocolat noir sans sucres" because it has a better
        nutriscore (C).
        """
        result = Product.objects.filter(name__iregex=r"^%s$" % "Chocolat bio")
        self.product = result.first()
        substit = self.product.find_substitute()
        if substit is not None:
            substit = substit.first()
            self.assertEqual(substit.name, "Chocolat noir sans sucres")


class FavorisTestCase(FillDbTestCase):
    """FavorisTestCase class."""

    def setUp(self):
        """Make Setup."""

        self.factory = RequestFactory()
        request = self.factory.get("/favorites")
        self.user = User.objects.create_user(
            username="bob", email="bob@bebo.com", password="poufpouf"
        )
        products = {"product_id": 1, "ref_product_id": 2}
        ref_product_id = products["ref_product_id"]
        ref_product = Product.objects.get(pk=ref_product_id)

        for item_id in products:
            if Substitutes.objects.filter(
                product_id=item_id,
                reference_id=ref_product.id,
                user_id=request.user.id,
            ).exists():
                pass

            else:
                substitute = Substitutes(
                    product_id=item_id,
                    reference_id=ref_product.id,
                    user_id=request.user.id,
                )
                substitute.save()


def test_favoris_status_code_200(self):
    """Test favoris status_code 200."""
    request = self.factory.get("/favorites")
    request.user = self.user
    response = favorites(request)
    self.assertEqual(response.status_code, 200)


def test_favoris_per_user(self):
    """Test favoris per user."""
    request = self.factory.get("/favorites")
    request.user = self.user
    breakpoint()
    res = Substitutes.objects.filter(user=request.user)
    self.assertEqual(res.name, "Chocolat noir sans sucres")


class ProductDetailsTestCase(FillDbTestCase):
    """FavorisTestCase class."""

    def setUp(self):
        """Make Setup."""
        self.factory = RequestFactory()
        self.product = Product.objects.get(name="Chocolat bio")

    def test_product_details_status_code_200(self):
        """Test product status_code 200."""
        request = self.factory.get("/product/Chocolat bio/")
        response = product_details(request, "Chocolat bio")
        self.assertEqual(response.status_code, 200)

    def test_product_details(self):
        """Test product."""
        self.assertEqual(self.product.name, "Chocolat bio")
