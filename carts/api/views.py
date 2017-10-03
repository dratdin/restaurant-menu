from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    )

from dishes.models import Dish
from carts.models import Cart

from carts.api.serializers import (
    CartListSerializer,
    CartDetailSerializer,
    CartCreateUpdateSerializer,
    )

from carts.api.permissions import (
    CartOwner,
    )

def enable_session_key(request):
    if not request.session.session_key:
        request.session.save()

def get_current_cart(request):
    enable_session_key(request)
    return Cart.current_cart(request.session)

class CartListAPIView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self, *args, **kwargs):
        get_current_cart(self.request)
        queryset = Cart.objects.filter(session_key=self.request.session.session_key)
        return queryset

class CartDetailAPIView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = [CartOwner,]    

class CurrentCartAPIView(APIView):
    queryset = Cart.objects.all()

    def get(self, request, format=None):
        current_cart = get_current_cart(request)
        serializer = CartListSerializer(current_cart)
        return Response(serializer.data)

class AddToCartAPIView(APIView):
    queryset = Cart.objects.all()

    def get(self, request, dish_id, quantity, format=None):
        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        current_cart = get_current_cart(request)
        current_cart.add_item(dish, dish.price, quantity)
        serializer = CartListSerializer(current_cart)
        return Response(serializer.data)

class RemoveItemFromCartAPIView(GenericAPIView):
    queryset = Cart.objects.all()
    permission_classes = [CartOwner,]
    serializer_class = CartDetailSerializer

    def get(self, request, pk, dish_id, *args, **kwargs):
        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart = self.get_object()
        cart.remove_item(dish)
        serializer = CartDetailSerializer(cart)
        return Response(serializer.data)