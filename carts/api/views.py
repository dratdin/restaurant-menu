from rest_framework.generics import (
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

def init_current_cart(request):
    enable_session_key(request)
    Cart.current_cart(request.session)

class CartListAPIView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self, *args, **kwargs):
        init_current_cart(self.request)
        queryset = Cart.objects.filter(session_key=self.request.session.session_key)
        print(queryset.count())
        return queryset

class CartDetailAPIView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = [CartOwner,]

class CartCreateAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateUpdateSerializer

    def perform_create(self, serializer):
        init_current_cart(self.request)
        serializer.save(session_key=self.request.session.session_key)

class CartUpdateAPIView(UpdateAPIView):
    serializer_class = CartCreateUpdateSerializer
    permission_classes = (CartOwner,)

class CartDeleteAPIView(DestroyAPIView):
    permission_classes = (CartOwner,)

    def perform_delete(self, serializer):
        serializer.delete(self.request.session)

# @enable_session_key
# def set_current_cart(request, id=None):
#     cart = Cart.get(request.session, id)
#     cart.set_as_current(request.session)
#     return redirect('carts:list')

# @enable_session_key
# def remove_from_cart(request, cart_id, dish_id):
#     dish = get_object_or_404(Dish, id=dish_id)
#     cart = Cart.get(request.session, cart_id)
#     cart.remove_item(dish)
#     if cart.is_current(request.session):
#         data = {
#             'current_cart_count': cart.count(),
#             'current_cart_sum': cart.summary()
#         }
#     else:
#         data = {}
#     return JsonResponse(data)
