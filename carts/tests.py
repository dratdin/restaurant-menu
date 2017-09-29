from django.test import TestCase
from django.test import Client

from carts.Cart import *
from carts.models import Cart as CartModel
from carts.forms import CartFormCreate
from dishes.models import Dish as DishModel
from dishes.models import Category as CategoryDish
from dishes.tests import create_drink_category, create_beer, create_orange_juice

class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session.save()
        self.cart_model = CartModel.objects.create(
            name="Cart1",
            description="Lala",
            session_key=self.session.session_key
        )
        drink_category = create_drink_category()
        create_beer(drink_category)
        create_orange_juice(drink_category)

    def test_cart_creating(self):
        cart_m = CartModel.objects.get(name="Cart1")
        self.assertRaises(CartCannotBeCreated, Cart)
        self.assertIsInstance(Cart(cart_m), Cart)
        self.assertIsInstance(Cart(session_key=cart_m.session_key), Cart)
        self.assertIsInstance(Cart(session_key=cart_m.session_key, name='For children', description='lallala'), Cart)

    def test_cart_update(self):
        cart = Cart.current_cart(self.session)
        name, description = cart.name, cart.description
        cart.update("CartUpdateName", "CartUpdateDescription")
        self.assertNotEqual(name, cart.name)
        self.assertNotEqual(description, cart.description)

    def test_cart_deleting(self):
        current_cart = Cart.current_cart(self.session)
        cart = Cart.add_new_cart(self.session, 'Cartka', 'dasdasdas')
        cart_id = cart.id
        cart.delete(self.session)
        with self.assertRaises(CartModel.DoesNotExist):
            cart_m = CartModel.objects.get(id=cart_id)
        with self.assertRaises(CurrentCartCantBeDeleted):
            current_cart.delete(self.session)

    def test_add_to_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Beer")
        cart.add_item(dish, dish.price, 1)
        self.assertEqual(cart.count(), 1)
        cart.add_item(dish, dish.price, 2)
        self.assertEqual(cart.count(), 3)

    def test_remove_from_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Beer")
        cart.add_item(dish, dish.price, 2)
        cart.remove_item(dish)
        self.assertEqual(cart.count(), 0)
        with self.assertRaises(ItemDoesNotExist):
            cart.remove_item(dish)

    def test_update_dish_in_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Beer")
        with self.assertRaises(ItemDoesNotExist):
            cart.update_item(dish, 2, dish.price)
        cart.add_item(dish, dish.price, 4)
        cart.update_item(dish, 2, dish.price)
        self.assertEqual(cart.count(), 2)

    def test_cart_summary(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        beer = DishModel.objects.get(name="Beer")
        orange_juice = DishModel.objects.get(name="Orange juice")
        beer_count = 2
        orange_juice_count = 3
        cart.add_item(beer, beer.price, beer_count)
        cart.add_item(orange_juice, orange_juice.price, orange_juice_count)
        self.assertEqual(
            cart.summary(),
            beer_count*beer.price + orange_juice_count*orange_juice.price
        )

    def test_cart_clear(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        beer = DishModel.objects.get(name="Beer")
        orange_juice = DishModel.objects.get(name="Orange juice")
        beer_count = 2
        orange_juice_count = 3
        cart.add_item(beer, beer.price, beer_count)
        cart.add_item(orange_juice, orange_juice.price, orange_juice_count)
        cart.clear()
        self.assertEqual(cart.count(), 0)

    def test_current_set_as_current(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        cart.set_as_current(self.session)
        self.assertEqual(cart.id, self.session[CART_ID])
        self.assertTrue(cart.is_current(self.session))

    def test_get_all_carts(self):
        carts = Cart.get_all_carts(self.session)
        count_carts_in_db = CartModel.objects.all().count()
        self.assertEqual(len(carts), count_carts_in_db)
        CartModel.objects.all().delete()
        with self.assertRaises(Http404):
            Cart.get_all_carts(self.session)

    def test_cart_get(self):
        other_session = Client().session
        other_session.save()
        cart_model = CartModel.objects.get(name="Cart1")
        cart_model_id = cart_model.id
        with self.assertRaises(Http404): # check if it isn't your cart
            cart = Cart.get(other_session, cart_model_id)
        cart_model.delete()
        with self.assertRaises(Http404):
            Cart.get(self.session, cart_model_id)

    def test_current_cart(self):
        # Case when session doesn't have cart_id
        current_cart = Cart.current_cart(self.session)
        self.assertIsInstance(current_cart, Cart)
        self.assertTrue(current_cart.is_current(self.session))
        # Case when session has legasy cart_id
        old_id = current_cart.id
        current_cart.cart.delete()
        current_cart = Cart.current_cart(self.session)
        self.assertIsInstance(current_cart, Cart)
        self.assertNotEqual(old_id, current_cart.id)
        # Case when session has valid cart_id
        cart_model = CartModel.objects.get(name="Cart1")
        cart = Cart(cart_model)
        cart.set_as_current(self.session)
        self.assertTrue(cart.is_current(self.session))
        current_cart = Cart.current_cart(self.session)
        self.assertEqual(cart.id, current_cart.id)
        cart_id = cart.id

    def test_view_cart_create_invalid(self):
        data = {
            # Cart with this name already exist for this session
            'name': 'Cart1',
            'description': "Lala",
        }
        response = self.client.post("/carts/create/", data)
        self.assertEqual(response.status_code, 200)


    def test_view_cart_create_valid(self):
        data = {
            'name': 'Cart2',
            'description': "lala",
        }
        response = self.client.post("/carts/create/", data)
        self.assertEqual(response.status_code, 302)
        CartModel.objects.get(name=data['name'])

    def test_view_cart_update_invalid(self):
        cart1 = CartModel.objects.get(name="Cart1")
        cart2 = CartModel.objects.create(
            name="Cart2",
            description="...",
            session_key=self.session.session_key
        )
        data = {
            # Cart with this name already exist for this session
            'name': cart2.name,
            'description': "Lala",
        }
        response = self.client.post("/carts/update/%d/" % cart1.id, data)
        self.assertEqual(response.status_code, 200)

    def test_view_cart_update_valid(self):
        cart = CartModel.objects.create(
            name="Cart2",
            description="...",
            session_key=self.session.session_key
        )
        data = {
            'name': "Cart 2 Updated!",
            'description': "±...±",
        }
        response = self.client.post("/carts/update/%d/" % cart.id, data)
        self.assertEqual(response.status_code, 302)
        CartModel.objects.get(name=data['name'])

    def test_cart_list_view(self):
        response = self.client.get("/carts/")
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_view(self):
        cart = Cart(self.cart_model)
        response = self.client.get(cart.get_absolute_url())
        self.assertEqual(response.status_code, 200)
