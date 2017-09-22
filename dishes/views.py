from django.shortcuts import render, get_object_or_404, Http404
from dishes.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request, category_alias=None):
    categories = Category.objects.all()
    category = Category.objects.filter(alias=category_alias)
    if category_alias is None:
        dishes = Dish.objects.all()
    else:
        dishes = Dish.objects.filter(category=category)
        if not dishes:
            raise Http404("Category not found")
    sort = request.GET.get('sort')
    if sort == 'asc':
        dishes = dishes.order_by('name')
    elif sort == 'desc':
        dishes = dishes.order_by('-name')
    paginator = Paginator(dishes, 6)
    page = request.GET.get('page')
    try:
        dishes = paginator.page(page)
    except PageNotAnInteger:
        dishes = paginator.page(1)
    except EmptyPage:
        dishes = paginator.page(paginator.num_pages)
    context = {
        'dishes': dishes,
        'categories': categories,
        'sort': sort
    }
    return render(request, 'index.html', context)

def detail(request, alias=None):
    dish = get_object_or_404(Dish, alias=alias)
    categories = Category.objects.all()
    context = {
        'dish': dish,
        'categories': categories,
    }
    return render(request, 'dish.html', context)
