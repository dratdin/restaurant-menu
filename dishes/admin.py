from django.contrib import admin
from dishes.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
