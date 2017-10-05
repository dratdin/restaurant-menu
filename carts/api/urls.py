from django.conf.urls import include, url
from rest_framework import routers
from .views import (
    CartDetailAPIView,
    CartListAPIView,
    CartCreateAPIView,
    CartUpdateAPIView,
    CartDeleteAPIView,
    SetAsCurrentAPIView,
    CurrentCartAPIView,
    AddToCartAPIView,
    RemoveItemFromCartAPIView,
    )

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^$', CartListAPIView.as_view(), name='list'),
    url(r'^create/$', CartCreateAPIView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', CartUpdateAPIView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', CartDeleteAPIView.as_view(), name='delete'),
    url(r'^set-as-current/(?P<pk>\d+)/$', SetAsCurrentAPIView.as_view(), name='set-as-current'),
    url(r'^current/$', CurrentCartAPIView.as_view(), name='current'),
    url(r'^add-to-cart/(?P<dish_id>\d+)/(?P<quantity>\d+)/$',  AddToCartAPIView.as_view(), name='add-to-cart'),
    url(r'^remove-from-cart/(?P<pk>\d+)/(?P<dish_id>\d+)/$',  RemoveItemFromCartAPIView.as_view(), name='remove-from-cart'),
    url(r'^(?P<pk>\d+)/$', CartDetailAPIView.as_view(), name='detail'),
]
