from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework.exceptions import ValidationError

class NotUniqName(ValidationError):
    pass

from dishes.models import Dish

class CurrentCartCantBeDeleted(ValidationError):
    pass

class ItemDoesNotExist(ValidationError):
    pass

CART_PK = 'CART-PK'

def create_default_cart(session):
    DEFAULT_NAME = 'My first cart'
    DEFAULT_DESCRIPTION = 'Automatically created cart...'
    return Cart.objects.create(
        session_key=session.session_key, 
        name=DEFAULT_NAME, 
        description=DEFAULT_DESCRIPTION
    )

class Cart(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.TextField()
    session_key = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    
    @property
    def count(self):
        result = 0
        for item in self.item_set.all():
            result += 1 * item.quantity
        return result

    @property
    def summary(self):
        result = 0
        for item in self.item_set.all():
            result += item.total_price
        return result
        
    def clean(self):
        try:
            cart = Cart.objects.get(name=self.name, session_key=self.session_key)
            if cart.pk != self.pk:
                raise NotUniqName(detail='You already have cart with this name.')
        except Cart.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Cart, self).save(*args, **kwargs)
    
    def update(self, name, description):
        self.name = name
        self.description = description
        self.save()

    def delete(self, session=None, *args, **kwargs):
        if session is None:
            raise CurrentCartCantBeDeleted('Session argument was not passed')
        if self.is_current(session):
            raise CurrentCartCantBeDeleted('You cant delete current cart!')
        return super(Cart, self).delete(*args, **kwargs)
    
    def set_as_current(self, session):
        session[CART_PK] = self.pk
        session.save()

    def is_current(self, session):
        return self.pk == session.get(CART_PK, None)
    
    def get_absolute_url(self):
        return reverse('carts-api:detail', kwargs={"pk": self.pk})
    
    def add_item(self, dish, unit_price, quantity=1):
        try:
            item = Item.objects.get(
                cart=self,
                dish=dish,
            )
        except Item.DoesNotExist:
            item = Item()
            item.cart = self
            item.dish = dish
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def update_item(self, dish, quantity):
        try:
            item = Item.objects.get(
                cart=self,
                dish=dish,
            )
        except Item.DoesNotExist:
            raise ItemDoesNotExist("Cart item does not exist")
        else: #ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.quantity = int(quantity)
                item.save()

    def remove_item(self, dish):
        try:
            item = Item.objects.get(
                cart=self,
                dish=dish,
            )
        except Item.DoesNotExist:
            raise ItemDoesNotExist("Cart item does not exist")
        else:
            item.delete()

    def clear(self):
        for item in self.item_set.all():
            item.delete()

    def __iter__(self):
        for item in self.item_set.all():
            yield item

    def __str__(self):
        return self.name

    @staticmethod
    def current_cart(session):
        cart_pk = session.get(CART_PK)
        if cart_pk:
            try:
                cart = Cart.objects.get(pk=cart_pk, checked_out=False)
            except Cart.DoesNotExist:
                cart = create_default_cart(session)
                cart.set_as_current(session)
        else:
            cart = create_default_cart(session)
            cart.set_as_current(session)
        return cart

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-created_at',)

    def __unicode__(self):
        return unicode(self.created_at)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.dish.__class__.__name__)

    @property
    def total_price(self):
        return self.quantity * self.unit_price
