from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from dishes.models import Dish

class Cart(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.TextField()
    session_key = models.CharField(max_length=256)
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

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
