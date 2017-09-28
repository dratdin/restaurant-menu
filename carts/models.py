from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils import timezone

from dishes.models import Dish

class Cart(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.TextField()
    session_key = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    def clean(self):
        try:
            cart = Cart.objects.get(name=self.name, session_key=self.session_key)
            if int(cart.id) != int(self.id):
                raise ValidationError(
                    'You already have %(name)s cart, you need to choose another name',
                    params={'name': name},
                )
        except Cart.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Cart, self).save(*args, **kwargs)

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
