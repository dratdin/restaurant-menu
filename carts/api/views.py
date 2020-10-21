from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.api.permissions import CartOwner
from carts.api.serializers import (
    CartCreateUpdateSerializer,
    CartDetailSerializer,
    CartListSerializer,
    CartSerializer,
)
from carts.models import Cart
from dishes.models import Dish


def get_current_cart(request):
    if not request.session.session_key:
        request.session.save()
    return Cart.get_current_cart(request.session)


class CartCreateAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateUpdateSerializer

    def perform_create(self, serializer):
        if not self.request.session.session_key:
            self.request.session.save()
        serializer.save(session_key=self.request.session.session_key)


class CartUpdateAPIView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateUpdateSerializer
    permission_classes = (CartOwner,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CartDeleteAPIView(GenericAPIView):
    queryset = Cart.objects.all()
    permission_classes = (CartOwner,)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.delete(request.session)
        carts = Cart.objects.filter(session_key=request.session.session_key)
        current_cart = get_current_cart(self.request)
        serializer = CartListSerializer(
            {"carts": carts, "current_cart_pk": current_cart.pk}
        )
        return Response(serializer.data)


class CartListAPIView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Cart.objects.filter(session_key=self.request.session.session_key)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        current_cart = get_current_cart(self.request)
        serializer = CartListSerializer(
            {"carts": queryset, "current_cart_pk": current_cart.pk}
        )
        return Response(serializer.data)


class CartDetailAPIView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = (CartOwner,)


class SetAsCurrentAPIView(GenericAPIView):
    queryset = Cart.objects.all()
    permission_classes = (CartOwner,)

    def get(self, request, pk, format=None):
        cart = self.get_object()
        cart.set_as_current(request.session)
        return Response({"current_cart_pk": cart.pk}, status=status.HTTP_202_ACCEPTED)


class CurrentCartAPIView(APIView):
    queryset = Cart.objects.all()

    def get(self, request, format=None):
        current_cart = get_current_cart(request)
        serializer = CartSerializer(current_cart)
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
        serializer = CartSerializer(current_cart)
        return Response(serializer.data)


class RemoveItemFromCartAPIView(GenericAPIView):
    queryset = Cart.objects.all()
    permission_classes = (CartOwner,)
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
