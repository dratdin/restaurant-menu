from django.shortcuts import render
from django.http import Http404
from dishes.models import *

def index(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    context = {
        'dishes': dishes,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def dish(request, alias):
    try:
        dish = Dish.objects.get(alias=alias)
    except:
        raise Http404("Dish not found")
    categories = Category.objects.all()
    context = {
        'dish': dish,
        'categories': categories,
    }
    return render(request, 'dish.html', context)
