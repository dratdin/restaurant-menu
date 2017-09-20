from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from carts.exceptions import CurrentCartCantBeDeleted
from carts.models import Cart, Item
from dishes.tests import create_beer, create_drink_category, create_orange_juice


class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.session.save()
        self.drink_category = create_drink_category()
        self.beer = create_beer(self.drink_category)
        self.orange_juice = create_orange_juice(self.drink_category)
        self.cart = Cart.objects.create(
            name="Cart1",
            description="Lala",
            session_key=self.client.session.session_key,
        )

    def test_cart_creating(self):
        self.assertIsInstance(self.cart, Cart)

    def test_cart_creating_invalid(self):
        """
        Create cart with existing name for this client
        """
        with self.assertRaises(ValidationError):
            Cart.objects.create(
                name=self.cart.name,
                description="Lala",
                session_key=self.client.session.session_key,
            )

    def test_cart_update(self):
        name, description = "New name for Cart1", "New description for Cart1"
        self.cart.update(name, description)
        self.assertEqual(self.cart.name, name)
        self.assertEqual(self.cart.description, description)

    def test_cart_update_invalid(self):
        """
        Update cart with existing name for this client
        """
        new_cart = Cart.objects.create(
            name="Cart2",
            description="Lala",
            session_key=self.client.session.session_key,
        )
        new_cart.name = self.cart.name
        new_cart.description = self.cart.description
        with self.assertRaises(ValidationError):
            new_cart.save()

    def test_cart_delete(self):
        deleted_cart_pk = self.cart.pk
        self.cart.delete(self.client.session)
        with self.assertRaises(Cart.DoesNotExist):
            Cart.objects.get(pk=deleted_cart_pk)

    def test_cart_delete_invalid(self):
        """
        Try to delete current cart
        """
        self.cart.set_as_current(self.client.session)
        with self.assertRaises(CurrentCartCantBeDeleted):
            self.cart.delete(self.client.session)

    def test_add_to_cart(self):
        self.cart.add_item(self.beer, self.beer.price, 1)
        self.assertEqual(self.cart.count, 1)
        self.cart.add_item(self.beer, self.beer.price, 2)
        self.assertEqual(self.cart.count, 3)

    def test_update_item_in_cart(self):
        with self.assertRaises(Item.DoesNotExist):
            self.cart.update_item(self.beer, 2)
        self.cart.add_item(self.beer, self.beer.price, 2)
        self.cart.update_item(self.beer, 1)
        self.assertEqual(self.cart.count, 1)

    def test_remove_from_cart(self):
        self.cart.add_item(self.beer, self.beer.price, 2)
        self.cart.remove_item(self.beer)
        self.assertEqual(self.cart.count, 0)
        with self.assertRaises(Item.DoesNotExist):
            self.cart.remove_item(self.beer)

    def test_clear_cart(self):
        self.cart.add_item(self.beer, self.beer.price, 4)
        self.cart.add_item(self.orange_juice, self.orange_juice.price, 2)
        self.cart.clear()
        self.assertEqual(self.cart.count, 0)

    def test_current_cart(self):
        # Case when session doesn't have cart_pk
        current_cart = Cart.get_current_cart(self.client.session)
        self.assertIsInstance(current_cart, Cart)
        self.assertTrue(current_cart.is_current(self.client.session))
        # Case when session has valid cart_pk
        self.cart.set_as_current(self.client.session)
        self.assertTrue(self.cart.is_current(self.client.session))
        current_cart = Cart.get_current_cart(self.client.session)
        self.assertEqual(self.cart.pk, current_cart.pk)
