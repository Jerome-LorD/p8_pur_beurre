"""Tests purbeurre models module."""


from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from purapps.purbeurre.models import Category, Product, Nutriscore, Substitutes


User = get_user_model()


class FillDbTestCase(TestCase):
    """FindSubstitutesTestCase class."""

    def setUp(self):
        """Make Setup."""
        products = [
            {
                "product_name_fr": "Chocolat bio",
                "brands": "Cote d'Or",
                "image_small_url": "http://www.chocolat-bio",
                "nutriments": {"bli_100g": "bli"},
                "url": "http://urltest.chocolat-bio",
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

        password = make_password("poufpouf")
        self.user, _ = User.objects.get_or_create(username="bob", password=password)

        for product in products:

            Nutriscore.objects.update_or_create(
                type=product["nutriscore_grade"],
                defaults={"type": product["nutriscore_grade"]},
            )

            last_nut = Nutriscore.objects.filter(
                type=product["nutriscore_grade"]
            ).values("id")

            Product.objects.update_or_create(
                name=product["product_name_fr"],
                defaults={
                    "name": product["product_name_fr"],
                    "url": product["url"],
                    "brand": product["brands"],
                    "nutriments": {
                        f"{k}": v
                        for k, v in product["nutriments"].items()
                        if "100g" in k
                    },
                    "image": product["image_small_url"],
                    "nutriscore_id": last_nut,
                },
            )

            for category in product["categories"].split(","):
                categorie = category.strip()

                Category.objects.update_or_create(
                    name=categorie, defaults={"name": categorie}
                )

                prod = Product.objects.get(name=product["product_name_fr"])

                category = Category.objects.filter(name=categorie).values("id").first()

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


class FavoritesTestCase(FillDbTestCase):
    """FavorisTestCase class."""

    def setUp(self):
        """Make Setup."""
        super().setUp()

        self.client = Client()

        product = Product.objects.get(name="Chocolat bio")
        substitute = Product.objects.get(name="Chocolat noir sans sucres")
        Substitutes.objects.create(
            reference=product, product=substitute, user=self.user
        )

    def test_favorites_status_code_200(self):
        """Test favoris status_code 200."""
        self.client.force_login(self.user)
        response = self.client.get("/favorites/")
        self.assertEqual(response.status_code, 200)

    def test_favorites_per_user(self):
        """Test favoris per user."""
        self.client.force_login(self.user)
        res = Substitutes.objects.filter(user=self.user).first()

        self.assertEqual(res.product.name, "Chocolat noir sans sucres")

    def test_favorites_page(self):
        """Test favorites page."""
        self.client.force_login(self.user)
        response = self.client.get("/favorites/")
        products = response.context["products"]

        self.assertIn(1, [product.id for product in products])


class ProductDetailsTestCase(FillDbTestCase):
    """ProductDetailsTestCase class."""

    def setUp(self):
        """Make Setup."""
        super().setUp()
        self.client = Client()
        self.product = Product.objects.get(name="Chocolat bio")

    def test_product_details_status_code_200(self):
        """Test product status_code 200."""
        response = self.client.get("/product/Chocolat bio/")
        self.assertEqual(response.status_code, 200)

    def test_product_details_name(self):
        """Test product name."""
        self.assertEqual(self.product.name, "Chocolat bio")

    def test_product_details_image(self):
        """Test product image."""
        self.assertEqual(self.product.image, "http://www.chocolat-bio")

    def test_product_details_nutriments(self):
        """Test product nutriments."""
        self.assertEqual(self.product.nutriments, {"bli_100g": "bli"})

    def test_product_details_url(self):
        """Test product url."""
        self.assertEqual(self.product.url, "http://urltest.chocolat-bio")


class IndexTestCase(TestCase):
    """IndexTestCase class."""

    def setUp(self):
        """Make Setup."""
        self.client = Client()

    def test_index_status_code_200(self):
        """Test index status_code 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class UrlsTestCase(TestCase):
    """UrlsTestCase class."""

    def test_urls(self):
        """Test Urls."""
        url = reverse("results", args=["Coca"])
        self.assertEqual(url, "/results/Coca/")

        url = reverse("product", args=["Coca-cola"])
        self.assertEqual(url, "/product/Coca-cola/")


class ProductModelTestCase(FillDbTestCase):
    """ProductModelTestCase class."""

    def setUp(self):
        """Make Setup."""
        super().setUp()

    def test_name_label(self):
        """Test name label."""
        product = Product.objects.get(name="Chocolat bio")
        field_label = product._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        """Test name max_length 240."""
        product = Product.objects.get(name="Chocolat bio")
        max_length = product._meta.get_field("name").max_length
        self.assertEquals(max_length, 240)


class ResultsTestCase(FillDbTestCase):
    """ResultsTestCase class."""

    def setUp(self):
        """Make Setup."""
        super().setUp()

    def test_results_status_code_200(self):
        """Test results status_code 200."""
        response = self.client.get("/results/Chocolat bio/")
        self.assertEqual(response.status_code, 200)

    def test_results_product_is_none(self):
        """Test results if product is None."""
        self.product = Product.objects.filter(name__iregex=r"^%s$" % "bretelle").first()
        self.assertIsNone(self.product, msg=None)
