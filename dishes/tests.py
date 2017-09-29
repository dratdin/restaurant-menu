from django.test import TestCase
from django.test import Client

from carts.Cart import *
from dishes.models import Dish
from dishes.models import Category

def create_drink_category():
    return Category.objects.create(name="Drinks", slug="drinks")

def create_beer(category):
    return Dish.objects.create(
        name="Beer",
        description="...",
        price=1.25,
        slug="beer",
        image="dishes/fixtures/drinks/beer.png",
        category=category
    )

def create_orange_juice(category):
    return Dish.objects.create(
        name="Orange juice",
        description="...",
        price=2.00,
        slug="orange-juice",
        image="dishes/fixtures/drinks/orange-juice.jpeg",
        category=category
    )

class CartTestCase(TestCase):
    def setUp(self):
        self.drink_category = create_drink_category()
        self.beer = create_beer(self.drink_category)
        self.orange_juice = create_orange_juice(self.drink_category)

    def test_category_and_dish_creating(self):
        self.assertIsInstance(self.drink_category, Category)
        self.assertIsInstance(self.beer, Dish)

    def test_dish_detail_view(self):
        response = self.client.get(self.beer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_dish_detail_view_invalid_slug(self):
        response = self.client.get('/dishes/%s/' % 'not-existing-dish')
        self.assertEqual(response.status_code, 404)

    def test_dish_list_empty_params(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dish_list_valid_category(self):
        response = self.client.get('/dishes/category/%s/' % self.drink_category.slug)
        self.assertEqual(response.status_code, 200)

    def test_dish_list_invalid_category(self):
        response = self.client.get('/dishes/category/%s/' % 'not-existing-category')
        self.assertEqual(response.status_code, 404)
