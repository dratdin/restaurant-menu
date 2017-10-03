from django.conf.urls import include, url
from rest_framework import routers
from .views import (
    CartDetailAPIView,
    CartListAPIView,
    AddToCartAPIView,
    CurrentCartAPIView,
    RemoveItemFromCartAPIView,
    )

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^$', CartListAPIView.as_view(), name='list'),
    url(r'^current/$', CurrentCartAPIView.as_view(), name='current'),
    url(r'^add-to-cart/(?P<dish_id>\d+)/(?P<quantity>\d+)/$',  AddToCartAPIView.as_view(), name='add-to-cart'),
    url(r'^remove-from-cart/(?P<pk>\d+)/(?P<dish_id>\d+)/$',  RemoveItemFromCartAPIView.as_view(), name='remove-from-cart'),
    url(r'^(?P<pk>\d+)/$', CartDetailAPIView.as_view(), name='detail'),
]
