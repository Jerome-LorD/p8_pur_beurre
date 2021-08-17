"""Tests purbeurre models module."""
from django.contrib.auth import get_user_model
from purapps.purbeurre.models import Category, Product, Nutriscore, Substitutes
from django.test import TestCase


# class ProductTestCase(TestCase):
#     """ProductTestCase class."""

#     def setUp(self):
#         """Make Setup."""
#         Product.objects.create(
#             name="café",
#             brand="bla",
#             stores="bli",
#             image="blo",
#             nutriments={"tst": 123},
#             url="http://chocolate.com",
#             nutriscore_id=self.nutriscore.id,
#         )
#         Product.objects.create(
#             name="chocolat",
#             brand="bla",
#             stores="bli",
#             image="blo",
#             nutriments={"tst": 123},
#             url="http://coffee.com",
#             nutriscore_id=self.nutriscore.id,
#         )

#         print(self.nutriscore.id)

#     @classmethod
#     def setUpTestData(cls):
#         """SetUp fk."""
#         cls.nutriscore = Nutriscore.objects.create(type="a")

#     def test_create_product(self):
#         """test created products."""
#         coffee = Product.objects.get(name="café")
#         chocolate = Product.objects.get(name="chocolat")
#         self.assertEqual(coffee.name, "café")
#         self.assertEqual(chocolate.name, "chocolat")


# class CategoryTestCase(TestCase):
#     """CategoryTestCase class."""

#     def setUp(self):
#         """Make Setup."""
#         Category.objects.create(name="chocolat")

#     def test_create_category(self):
#         """Test created categories."""
#         cat_chocolate = Category.objects.get(name="chocolat")
#         self.assertEqual(cat_chocolate.name, "chocolat")


# class NutriscoreTestCase(TestCase):
#     """NutriscoreTestCase class."""

#     def setUp(self):
#         """Make Setup."""
#         Nutriscore.objects.create(type="a")

#     def test_create_Nutriscore(self):
#         """Test created nutriscore."""
#         nutriscore = Nutriscore.objects.get(pk=1)
#         self.assertEqual(nutriscore.type, "a")


# class SubstitutesTestCase(TestCase):
#     """SubstitutesTestCase class."""

#     def setUp(self):
#         """Make Setup."""
#         User = get_user_model()
#         self.user = User.objects.create(username="machin", password="poufpouf")

#     @classmethod
#     def setUpTestData(cls):
#         """Set Up fk."""
#         cls.product = Product.objects.get(name="chocolat")
#         cls.reference = Product.objects.get(name="café")

#     def test_create_user(self):
#         """Test created user."""
#         user = Substitutes.objects.get(user_id=1)
#         self.assertEqual(user.id, 1, self.product.id, self.reference.id)


class FindSubstitutesTestCase(TestCase):
    """FindSubstitutesTestCase class."""

    def setUp(self):
        """Make Setup."""
        nutriscore_type_B = Nutriscore.objects.create(type="b")
        nutriscore_type_E = Nutriscore.objects.create(type="e")

        Category.objects.create(name="Cat A")
        category_a = Category.objects.filter(name="Cat A").values("id")[0]

        self.prod_a = Product.objects.create(
            name="produit A",
            brand="marque A",
            image="http image A",
            nutriments={"bla": "bla"},
            url="http A",
            nutriscore=nutriscore_type_E,
        )
        self.prod_b = Product.objects.create(
            name="produit B",
            brand="marque B",
            image="http image B",
            nutriments={"bla": "bla"},
            url="http B",
            nutriscore=nutriscore_type_B,
        )
        self.prod_c = Product.objects.create(
            name="produit C",
            brand="marque B",
            image="http image C",
            nutriments={"bla": "bla"},
            url="http C",
            nutriscore=nutriscore_type_E,
        )
        self.prod_d = Product.objects.create(
            name="produit D",
            brand="marque B",
            image="http image D",
            nutriments={"bla": "bla"},
            url="http D",
            nutriscore=nutriscore_type_E,
        )
        self.prod_e = Product.objects.create(
            name="produit E",
            brand="marque B",
            image="http image E",
            nutriments={"bla": "bla"},
            url="http E",
            nutriscore=nutriscore_type_E,
        )

        lst = ["produit A", "produit B", "produit C", "produit D", "produit E"]
        for i in lst:

            self.prod = Product.objects.get(name=i)
            self.prod.categories.add(category_a.get("id"))

        self.product = Product.objects.get(pk=self.prod_d.id)

    def test_find_substitute(self):
        """Test find substitutes."""
        substit = Product.find_substitute(self.product.id)
        substit = substit.first()
        self.assertEqual(substit.name, "produit B")
