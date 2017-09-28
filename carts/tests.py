from django.test import TestCase
from django.test import Client

from carts.Cart import *
from carts.models import Cart as CartModel
from carts.forms import CartForm
from dishes.models import Dish as DishModel
from dishes.models import Category as CategoryDish
from dishes.tests import create_drink_category, create_apple_juice, create_orange_juice

class CartTestCase(TestCase):
    def setUp(self):
        self.session = self.client.session
        self.session.save()
        CartModel.objects.create(
            name="Cart1",
            description="Lala",
            session_key=self.session.session_key
        )
        drink_category = create_drink_category()
        create_apple_juice(drink_category)
        create_orange_juice(drink_category)

    def test_cart_creating(self):
        cart_m = CartModel.objects.get(name="Cart1")
        self.assertRaises(CartCannotBeCreated, Cart)
        self.assertIsInstance(Cart(cart_m), Cart)
        self.assertIsInstance(Cart(session_key=cart_m.session_key), Cart)
        self.assertIsInstance(Cart(session_key=cart_m.session_key, name='For children', description='lallala'), Cart)

    def test_add_to_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Apple juice")
        cart.add(dish, dish.price, 1)
        self.assertEqual(cart.count(), 1)
        cart.add(dish, dish.price, 2)
        self.assertEqual(cart.count(), 3)

    def test_remove_from_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Apple juice")
        cart.add(dish, dish.price, 2)
        cart.remove(dish)
        self.assertEqual(cart.count(), 0)
        with self.assertRaises(ItemDoesNotExist):
            cart.remove(dish)

    def test_update_dish_in_cart(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        dish = DishModel.objects.get(name="Apple juice")
        with self.assertRaises(ItemDoesNotExist):
            cart.update(dish, 2, dish.price)
        cart.add(dish, dish.price, 4)
        cart.update(dish, 2, dish.price)
        self.assertEqual(cart.count(), 2)

    def test_cart_summary(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        apple_juice = DishModel.objects.get(name="Apple juice")
        orange_juice = DishModel.objects.get(name="Orange juice")
        apple_juice_count = 2
        orange_juice_count = 3
        cart.add(apple_juice, apple_juice.price, apple_juice_count)
        cart.add(orange_juice, orange_juice.price, orange_juice_count)
        self.assertEqual(
            cart.summary(),
            apple_juice_count*apple_juice.price + orange_juice_count*orange_juice.price
        )

    def test_cart_clear(self):
        cart = Cart(CartModel.objects.get(name="Cart1"))
        apple_juice = DishModel.objects.get(name="Apple juice")
        orange_juice = DishModel.objects.get(name="Orange juice")
        apple_juice_count = 2
        orange_juice_count = 3
        cart.add(apple_juice, apple_juice.price, apple_juice_count)
        cart.add(orange_juice, orange_juice.price, orange_juice_count)
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

    def test_create_new_cart_invalidform_view(self):
        data = {
            # Cart with this name already exist for this session
            'name': 'Cart1',
            'description': "Lala",
        }
        response = self.client.post("/carts/create/", data)
        self.assertEqual(response.status_code, 200)


    def test_create_new_cart_validform_view(self):
        data = {
            'name': 'Cart2',
            'description': "lala",
        }
        response = self.client.post("/carts/create/", data)
        self.assertEqual(response.status_code, 302)
        CartModel.objects.get(name=data['name'])
