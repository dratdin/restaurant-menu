from django.test import TestCase
from django.test import Client

from django.http import HttpRequest

from carts.Cart import Cart
from carts import models


class CartTestCase(TestCase):
    def setUp(self):
        m_cart1 = models.Cart(
            name="My little cart",
            description="Lala",
            session_key="plokijuhygt"
        )

    def test_cart_get(self):
        cart = Cart(
            m_cart1
        )
        self.assertEqual(Cart.get(m_cart1.session_key, m_cart1.id), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
