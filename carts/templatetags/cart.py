from django import template
from carts.Cart import Cart

register = template.Library()

@register.simple_tag()
def current_cart(request):
    cart = Cart.current_cart(request)
    return cart
