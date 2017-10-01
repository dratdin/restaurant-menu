from django.conf.urls import include, url
from rest_framework import routers
from .views import (
    CartDetailAPIView,
    CartListAPIView,
    CartCreateAPIView,
    CartUpdateAPIView,
    CartDeleteAPIView,
    )

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^$', CartListAPIView.as_view(), name='list'),
    url(r'^create/$', CartCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CartDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', CartUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', CartDeleteAPIView.as_view(), name='delete'),
    url(r'^add-to-cart/(?P<dish_id>\d+)/(?P<quantity>\d+)/$', CartDeleteAPIView.as_view(), name='add-to-cart'),
]
