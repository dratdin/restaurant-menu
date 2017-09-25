import datetime
from django.shortcuts import get_object_or_404, get_list_or_404, Http404
from django.core.urlresolvers import reverse

from . import models

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    """
        request - from view request
        **kargs
            Expected arguments
            object_model - object of models.Cart
            name
            description
    """
    def __init__(self, request, object_model=None, **kwargs):
        if object_model is not None:
            cart = object_model
        else:
            name = kwargs.get('name', "My first cart")
            description = kwargs.get('description', "Automaticaly created cart")
            cart = self.new(request, name, description)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request, name, description):
        if not request.session.get('has_session'):
            request.session['has_session'] = True
        cart = models.Cart(name=name, description=description, session_key=request.session.session_key, creation_date=datetime.datetime.now())
        cart.save()
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
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
        print(request.session[CART_ID])

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
    def current_cart(request):
        cart_id = request.session.get(CART_ID)
        print('POINT 1 ±±±±±±±±±±±±±±±±±±±±±±±±±')
        print(cart_id)
        print(request.session.session_key)
        if cart_id:
            try:
                cart_model = models.Cart.objects.get(id=cart_id, checked_out=False)
                cart = Cart(request, cart_model)
                print('POINT 2 ±±±±±±±±±±±±±±±±±±±±±±±±±')
            except models.Cart.DoesNotExist:
                cart = Cart(request)
                cart.set_as_current(request)
                print('POINT 3 ±±±±±±±±±±±±±±±±±±±±±±±±±')
        else:
            cart = Cart(request)
            cart.set_as_current(request)
            print('POINT 4 ±±±±±±±±±±±±±±±±±±±±±±±±±')
        return cart

    @staticmethod
    def add_new_cart(request, name, description):
        cart = Cart(request, name=name, description=description)
        return cart

    @staticmethod
    def get_all_carts(request):
        carts_model = models.Cart.objects.filter(session_key=request.session.session_key)
        carts = []
        for cart_model in carts_model:
            carts.append(Cart.get(request, cart_model.id))
        return carts

    @staticmethod
    def get(request, id):
        cart_model = get_object_or_404(models.Cart, id=id, checked_out=False)
        if request.session.session_key == cart_model.session_key:
            return Cart(request, cart_model)
        else:
            raise Http404("It isn't your cart!")
