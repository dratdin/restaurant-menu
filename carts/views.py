from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import JsonResponse

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
    """ Add product to current cart"""
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.current_cart(request.session)
    cart.add(dish, dish.price, quantity)
    data = {
        'current_cart_count': cart.count(),
        'current_cart_sum': cart.summary()
    }
    return JsonResponse(data)

def remove_from_cart(request, cart_id, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.get(request.session, cart_id)
    cart.remove(dish)
    if cart.is_current(request.session):
        data = {
            'current_cart_count': cart.count(),
            'current_cart_sum': cart.summary()
        }
    else:
        data = {}
    return JsonResponse(data)

@enable_session_key
def cart_detail(request, id=None):
    cart = Cart.get(request.session, id)
    context = { 'cart': cart }
    return render(request, 'detail.html', context)

@enable_session_key
def cart_list(request):
    carts = Cart.get_all_carts(request.session)
    context = {
        'carts': carts,
    }
    return render(request, 'carts.html', context)

@enable_session_key
def cart_create(request):
    if request.method == 'POST':
        form = CartForm(request.POST, request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Cart.add_new_cart(request.session, name, description)
            return redirect('carts:list')
    else:
        form = CartForm()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)

@enable_session_key
def set_current_cart(request, id=None):
    cart = Cart.get(request.session, id)
    cart.set_as_current(request.session)
    return redirect('carts:list')
