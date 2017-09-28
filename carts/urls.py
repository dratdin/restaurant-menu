from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from .views import (
    cart_detail,
    cart_list,
    cart_create,
    cart_update,
    cart_delete,
    add_to_cart,
    remove_from_cart,
    set_current_cart,
    )

urlpatterns = [
    url(r'^$', cart_list, name='list'),
    url(r'^detail/(?P<id>\d+)/$', cart_detail, name='detail'),
    url(r'^create/', cart_create, name='create'),
    url(r'^update/(?P<id>\d+)/$', cart_update, name='update'),
    url(r'^delete/(?P<id>\d+)/$', cart_delete, name='delete'),
    url(r'^set-current/(?P<id>\d+)/$', set_current_cart, name='set_current'),
    url(r'^add/(?P<dish_id>\d+)/(?P<quantity>\d+)/$', add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<cart_id>\d+)/(?P<dish_id>\d+)/$', remove_from_cart, name='remove_from_cart'),
]
