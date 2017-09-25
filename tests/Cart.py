from django.test import TestCase
from django.test import Client

from carts.Cart import Cart

# class CartTestCase(TestCase):
#     def setUp(self):
#         cart_init = Cart(
#             name="My little cart",
#             description="Lala",
#             )

#     def test_cart_creating(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')
