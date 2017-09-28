import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404, Http404

from . import models

CART_ID = 'CART-ID'

class CartCannotBeCreated(Exception):
    pass

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class CurrentCartCantBeDeleted(Exception):
    pass

class Cart:
    """
        Before usenig all methods of these class
        you need check session_key existance
        except current_cart method. It checks session_key by itself
    """
    def __init__(self, object=None, **kwargs):
        """
            object - existing object of Cart model
            **kargs
                Expected arguments
                name
                description
                session_key
        """
        if object is not None:
            cart = object
        else:
            if 'session_key' in kwargs:
                session_key = kwargs.get('session_key')
                if session_key is None:
                    raise CartCannotBeCreated('Session key is None!')
                else:
                    name = kwargs.get('name', "My first cart")
                    description = kwargs.get('description', "Automaticaly created cart")
                    cart = self.new(session_key, name, description)
            else:
                raise CartCannotBeCreated('Session key not passed!')
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, session_key, name, description):
        cart = models.Cart(session_key=session_key, name=name, description=description)
        cart.save()
        return cart

    def update(self, name, description):
        self.cart.name = name
        self.cart.description = description
        self.cart.save()

    def delete(self, session):
        if self.is_current(session):
            raise CurrentCartCantBeDeleted
        else:
            self.cart.delete()

    def add_item(self, dish, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                dish=dish,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.dish = dish
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def remove_item(self, dish):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                dish=dish,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist("Cart item does not exist")
        else:
            item.delete()

    def update_item(self, dish, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                dish=dish,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else: #ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()

    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result

    def summary(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def get_absolute_url(self):
        return reverse('carts:detail', kwargs={"id": self.id})

    def set_as_current(self, session):
        session[CART_ID] = self.id

    def is_current(self, session):
        return self.id == session[CART_ID]

    # PROPERTIES
    @property
    def session_key(self):
        return self.cart.session_key

    @property
    def id(self):
        return self.cart.id

    @property
    def name(self):
        return self.cart.name

    @property
    def description(self):
        return self.cart.description

    # STATIC METHODS
    @staticmethod
    def get_all_carts(session):
        """
            Return list of carts whick belong to session
            Or raise Http404 if list is empty
        """
        carts_model = get_list_or_404(models.Cart, session_key=session.session_key)
        carts = []
        for cart_model in carts_model:
            carts.append(Cart(cart_model))
        return carts

    @staticmethod
    def get(session, id):
        cart_model = get_object_or_404(models.Cart, id=id, checked_out=False)
        if session.session_key == cart_model.session_key:
            return Cart(cart_model)
        else:
            raise Http404("It isn't your cart!")

    @staticmethod
    def add_new_cart(session, name, description):
        return Cart(session_key=session.session_key, name=name, description=description)

    @staticmethod
    def current_cart(session):
        """
            This is the only method which check the existence of session key
        """
        if not session.session_key:
            session.save()
        cart_id = session.get(CART_ID)
        if cart_id:
            try:
                cart_model = models.Cart.objects.get(id=cart_id, checked_out=False)
                cart = Cart(cart_model)
            except models.Cart.DoesNotExist:
                cart = Cart(session_key=session.session_key)
                cart.set_as_current(session)
        else:
            cart = Cart(session_key=session.session_key)
            cart.set_as_current(session)
        return cart
