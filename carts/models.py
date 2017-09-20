from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.models import TimeStampMixin
from dishes.models import Dish

from . import exceptions


class Cart(TimeStampMixin):
    CART_PK_SESSION_KEY = "CART-PK"

    DEFAULT_NAME = "My first cart"
    DEFAULT_DESCRIPTION = "Automatically created cart..."

    name = models.CharField(
        max_length=128, verbose_name=_("Name"), default=DEFAULT_NAME
    )
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    session_key = models.CharField(max_length=256)
    checked_out = models.BooleanField(default=False, verbose_name=_("checked out"))

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
                raise exceptions.NotUniqName("You already have cart with this name.")
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
            raise exceptions.CurrentCartCantBeDeleted("Session argument was not passed")
        if self.is_current(session):
            raise exceptions.CurrentCartCantBeDeleted("You cant delete current cart!")
        return super(Cart, self).delete(*args, **kwargs)

    def set_as_current(self, session):
        session[self.CART_PK_SESSION_KEY] = self.pk
        session.save()

    def is_current(self, session):
        return self.pk == session.get(self.CART_PK_SESSION_KEY, None)

    def get_absolute_url(self):
        return reverse("carts-api:detail", kwargs={"pk": self.pk})

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
        else:  # ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def update_item(self, dish, quantity):
        item = Item.objects.get(
            cart=self,
            dish=dish,
        )
        if quantity == 0:
            item.delete()
        else:
            item.quantity = int(quantity)
            item.save()

    def remove_item(self, dish):
        Item.objects.get(
            cart=self,
            dish=dish,
        ).delete()

    def clear(self):
        for item in self.item_set.all():
            item.delete()

    def __iter__(self):
        for item in self.item_set.all():
            yield item

    def __str__(self):
        return self.name

    @classmethod
    def get_current_cart(cls, session):
        cart_pk = session.get(cls.CART_PK_SESSION_KEY)
        if cart_pk:
            cart, is_created = Cart.objects.get_or_create(
                pk=cart_pk,
                checked_out=False,
                defaults={"session_key": session.session_key},
            )
            if is_created:
                cart.set_as_current(session)
        else:
            cart = cls.create_default_cart(session)
            cart.set_as_current(session)

        return cart

    @classmethod
    def create_default_cart(cls, session):
        return Cart.objects.create(session_key=session.session_key)

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ("-created_at",)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_("cart"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"))
    unit_price = models.DecimalField(
        max_digits=18, decimal_places=2, verbose_name=_("unit price")
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ("cart",)

    def __str__(self):
        return u"%d units of %s" % (self.quantity, type(self.dish))

    @property
    def total_price(self):
        return self.quantity * self.unit_price
