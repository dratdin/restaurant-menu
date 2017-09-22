# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from dishes.models import *

# def index(request, page=1):
#     dishes = Dish.objects.all()
#     categories = Category.objects.all()
#     paginator = Paginator(dishes, 6)
#     # page = request.GET.get('page')
#     try:
#         dishes = paginator.page(page)
#     except PageNotAnInteger:
#         dishes = paginator.page(1)
#     except EmptyPage:
#         dishes = paginator.page(paginator.num_pages)
#     context = {
#         'dishes': dishes,
#         'categories': categories,
#     }
#     return render(request, 'index.html', context)
