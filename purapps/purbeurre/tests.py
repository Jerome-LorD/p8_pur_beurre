"""Tests purbeurre models module."""
from purapps.purbeurre.models import Category, Product, Nutriscore
from django.test import TestCase

# from purbeurre.models import Product


class ProductTestCase(TestCase):
    """ProductTestCase class."""

    def setUp(self):
        """Make Setup."""
        Product.objects.create(
            name="café",
            brand="bla",
            stores="bli",
            image="blo",
            url="http://chocolate.com",
        )
        Product.objects.create(
            name="chocolat",
            brand="bla",
            stores="bli",
            image="blo",
            url="http://coffee.com",
        )

    def test_create_product(self):
        """test created products."""
        coffee = Product.objects.get(name="café")
        chocolate = Product.objects.get(name="chocolat")
        self.assertEqual(coffee.name, "café")
        self.assertEqual(chocolate.name, "chocolat")


class CategoryTestCase(TestCase):
    """CategoryTestCase class."""

    def setUp(self):
        """Make Setup."""
        Category.objects.create(name="chocolat")

    def test_create_category(self):
        """Test created categories."""
        cat_chocolate = Category.objects.get(name="chocolat")
        self.assertEqual(cat_chocolate.name, "chocolat")


class NutriscoreTestCase(TestCase):
    """NutriscoreTestCase class."""

    def setUp(self):
        """Make Setup."""
        Nutriscore.objects.create(type="a")

    def test_create_Nutriscore(self):
        """Test created nutriscore."""
        nutriscore = Nutriscore.objects.get(pk=1)
        self.assertEqual(nutriscore.type, "a")
