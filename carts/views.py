from django.shortcuts import render, redirect

from dishes.models import Dish
from carts.Cart import Cart
from .forms import CartForm

def add_to_cart(request, product_id, quantity):
    dish = Dish.objects.get(id=product_id)
    cart = Cart.current_cart(request)
    cart.add(dish, dish.price, quantity)
    return redirect('index')

def remove_from_cart(request, product_id):
    product = Dish.objects.get(id=product_id)
    cart = Cart.current_cart(request)
    cart.remove(product)
    context = {
        'cart': cart,
    }
    return render(request, 'cart_detail.html', context)

def cart_detail(request, id=None):
    cart = Cart.get(request, id)
    context = {'cart': cart}
    return render(request, 'cart_detail.html', context)

def cart_list(request):
    carts = Cart.get_all_carts(request)
    context = {
        'carts': carts,
    }
    return render(request, 'cart_list.html', context)

def cart_create(request):
    form = CartForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        Cart(request, name=name, description=description)
        return redirect('carts:list')
    context = {
        'form': form,
    }
    return render(request, 'cart_create.html', context)

def set_current_cart(request, id=None):
    cart = Cart.get(request, id)
    cart.set_as_current(request)
    return redirect('carts:list')
