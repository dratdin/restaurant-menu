from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r"^$", views.CartListAPIView.as_view(), name="list"),
    url(r"^create/$", views.CartCreateAPIView.as_view(), name="create"),
    url(r"^update/(?P<pk>\d+)/$", views.CartUpdateAPIView.as_view(), name="update"),
    url(r"^delete/(?P<pk>\d+)/$", views.CartDeleteAPIView.as_view(), name="delete"),
    url(
        r"^set-as-current/(?P<pk>\d+)/$",
        views.SetAsCurrentAPIView.as_view(),
        name="set-as-current",
    ),
    url(r"^current/$", views.CurrentCartAPIView.as_view(), name="current"),
    url(
        r"^add-to-cart/(?P<dish_id>\d+)/(?P<quantity>\d+)/$",
        views.AddToCartAPIView.as_view(),
        name="add-to-cart",
    ),
    url(
        r"^remove-from-cart/(?P<pk>\d+)/(?P<dish_id>\d+)/$",
        views.RemoveItemFromCartAPIView.as_view(),
        name="remove-from-cart",
    ),
    url(r"^(?P<pk>\d+)/$", views.CartDetailAPIView.as_view(), name="detail"),
]
