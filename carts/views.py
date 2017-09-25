from django.shortcuts import render, redirect, get_object_or_404, Http404

from dishes.models import Dish
from carts.Cart import *
from .forms import CartForm

class EnableSessionKeyNoRequestArgument(Exception):
    pass

def enable_session_key(function):
    def wrapper(request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        return function(request, *args, **kwargs)
    return wrapper

def add_to_cart(request, dish_id, quantity):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.current_cart(request)
    cart.add(dish, dish.price, quantity)
    return redirect('index')

def remove_from_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.current_cart(request)
    cart.remove(dish)
    context = {
        'cart': cart,
    }
    return render(request, 'cart_detail.html', context)

@enable_session_key
def cart_detail(request, id=None):
    cart = Cart.get(request.session.session_key, id)
    context = { 'cart': cart }
    return render(request, 'cart_detail.html', context)

@enable_session_key
def cart_list(request):
    carts = Cart.get_all_carts(request.session.session_key)
    context = {
        'carts': carts,
    }
    return render(request, 'cart_list.html', context)

@enable_session_key
def cart_create(request):
    if request.method == 'POST':
        form = CartForm(request.POST, request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Cart.add_new_cart(request.session.session_key, name=name, description=description)
            return redirect('carts:list')
    else:
        form = CartForm()
    context = {
        'form': form,
    }
    return render(request, 'cart_create.html', context)

@enable_session_key
def set_current_cart(request, id=None):
    cart = Cart.get(request.session.session_key, id)
    cart.set_as_current(request)
    return redirect('carts:list')
