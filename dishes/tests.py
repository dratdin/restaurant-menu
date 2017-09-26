from django.test import TestCase
from django.test import Client

from carts.Cart import *
from dishes.models import Dish
from dishes.models import Category

def create_drink_category():
    return Category.objects.create(name="Drinks", slug="drinks")

def create_apple_juice(category):
    return Dish.objects.create(
        name="Apple juice",
        description="...",
        price=1.25,
        slug="apple-juice",
        category=category
    )

def create_orange_juice(category):
    return Dish.objects.create(
        name="Orange juice",
        description="...",
        price=2.00,
        slug="apple-juice",
        category=category
    )

class CartTestCase(TestCase):
    def setUp(self):
        self.drink_category = create_drink_category()
        self.apple_juice = create_apple_juice(self.drink_category)
        self.orange_juice = create_orange_juice(self.drink_category)

    def test_category_and_dish_creating(self):
        self.assertIsInstance(self.drink_category, Category)
        self.assertIsInstance(self.apple_juice, Dish)
