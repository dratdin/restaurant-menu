from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dishes.models import *

from functools import wraps

def dish_list(request, category_slug=None):
    if category_slug is None:
        dishes = Dish.objects.all()
    else:
        category = get_object_or_404(Category, slug=category_slug)
        dishes = Dish.objects.filter(category=category)
    sort_param_name = 'sort'
    sort = request.GET.get(sort_param_name)
    if sort == 'asc':
        dishes = dishes.order_by('name')
    elif sort == 'desc':
        dishes = dishes.order_by('-name')
    paginator = Paginator(dishes, 6)
    page_param_name = 'page'
    page = request.GET.get(page_param_name)
    try:
        dishes = paginator.page(page)
    except PageNotAnInteger:
        dishes = paginator.page(1)
    except EmptyPage:
        dishes = paginator.page(paginator.num_pages)
    context = {
        'page_param_name': page_param_name,
        'dishes': dishes,
        'sort_param_name': sort_param_name,
        'sort': sort,
    }
    return render(request, 'index.html', context)

def dish_detail(request, slug=None):
    dish = get_object_or_404(Dish, slug=slug)
    context = {
        'dish': dish,
    }
    return render(request, 'dish_detail.html', context)
