import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404

from . import models

CART_ID = 'CART-ID'

class CartCannotBeCreated(Exception):
    pass

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    """
        **kargs
            Expected arguments
            object - object of models.Cart
            name
            description
            session_key
    """
    # +
    def __init__(self, object=None, **kwargs):
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
        cart = models.Cart(session_key=session_key, name=name, description=description, creation_date=datetime.datetime.now())
        cart.save()
        return cart

    def add(self, dish, unit_price, quantity=1):
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

    def remove(self, dish):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                dish=dish,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist("Cart item does not exist")
        else:
            item.delete()

    def update(self, dish, quantity, unit_price=None):
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

    def set_as_current(self, request):
        request.session[CART_ID] = self.id

    def is_current(self, request):
        return self.id == request.session[CART_ID]

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
        return self.description.name

    # STATIC METHODS

    @staticmethod
    def add_new_cart(session_key, name, description):
        cart = Cart(session_key=session_key, name=name, description=description)
        return cart

    @staticmethod
    def get_all_carts(session_key):
        carts_model = models.Cart.objects.filter(session_key=session_key)
        carts = []
        for cart_model in carts_model:
            carts.append(Cart(cart_model))
        return carts

    @staticmethod
    def get(session_key, id):
        cart_model = get_object_or_404(models.Cart, id=id, checked_out=False)
        if session_key == cart_model.session_key:
            return Cart(cart_model)
        else:
            raise Http404("It isn't your cart!")

    @staticmethod
    def current_cart(request):
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart_model = models.Cart.objects.get(id=cart_id, checked_out=False)
                cart = Cart(cart_model)
            except models.Cart.DoesNotExist:
                cart = Cart(session_key=session_key)
                cart.set_as_current(request)
        else:
            cart = Cart(session_key=session_key)
            cart.set_as_current(request)
        return cart
