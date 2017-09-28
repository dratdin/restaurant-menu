from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import JsonResponse

from dishes.models import Dish
from carts.Cart import *
from .forms import CartFormCreate, CartFormUpdate

class EnableSessionKeyNoRequestArgument(Exception):
    pass

def enable_session_key(function):
    def wrapper(request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        return function(request, *args, **kwargs)
    return wrapper

@enable_session_key
def cart_list(request):
    carts = Cart.get_all_carts(request.session)
    context = {
        'carts': carts,
    }
    return render(request, 'carts.html', context)

@enable_session_key
def cart_detail(request, id=None):
    cart = Cart.get(request.session, id)
    context = { 'cart': cart }
    return render(request, 'detail.html', context)

@enable_session_key
def cart_create(request):
    if request.method == 'POST':
        form = CartFormCreate(request.POST, request=request)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Cart.add_new_cart(request.session, name, description)
            return redirect('carts:list')
    else:
        form = CartFormCreate()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)

@enable_session_key
def cart_update(request, id=None):
    cart = Cart.get(request.session, id)
    if request.method == 'POST':
        form = CartFormUpdate(request.POST, request=request, id=id)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cart.update(name, description)
            return redirect('carts:list')
    else:
        form = CartFormUpdate(instance=cart.cart, id=id)
    context = {
        'form': form
    }
    return render(request, 'update.html', context)

@enable_session_key
def cart_delete(request, id=None):
    cart = Cart.get(request.session, id)
    cart.delete(request.session)
    return redirect('carts:list')

@enable_session_key
def set_current_cart(request, id=None):
    cart = Cart.get(request.session, id)
    cart.set_as_current(request.session)
    return redirect('carts:list')

@enable_session_key
def add_to_cart(request, dish_id, quantity):
    """ Add product to current cart"""
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.current_cart(request.session)
    cart.add_item(dish, dish.price, quantity)
    data = {
        'current_cart_count': cart.count(),
        'current_cart_sum': cart.summary()
    }
    return JsonResponse(data)

@enable_session_key
def remove_from_cart(request, cart_id, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart.get(request.session, cart_id)
    cart.remove_item(dish)
    if cart.is_current(request.session):
        data = {
            'current_cart_count': cart.count(),
            'current_cart_sum': cart.summary()
        }
    else:
        data = {}
    return JsonResponse(data)
