from django import template
from carts.Cart import Cart

register = template.Library()

@register.simple_tag()
def get_current_cart(request):
    return Cart.current_cart(request)
