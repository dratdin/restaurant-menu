from django.shortcuts import render
from dishes.models import *

def index(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    context = {
        'dishes': dishes,
        'categories': categories,
    }
    return render(request, 'index.html', context)
