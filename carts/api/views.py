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

class CartListAPIView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self, *args, **kwargs):
        enable_session_key(self.request)
        queryset = Cart.objects.filter(session_key=self.request.session.session_key)
        return queryset

class CartDetailAPIView(RetrieveAPIView):
    serializer_class = CartDetailSerializer
    permission_classes = [CartOwner,]

    def get_queryset(self, *args, **kwargs):
        enable_session_key(self.request)
        queryset = Cart.objects.all()
        return queryset

class CartCreateAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(session_key=self.request.session.session_key)

class CartUpdateAPIView(UpdateAPIView):
    serializer_class = CartCreateUpdateSerializer
    permission_classes = (CartOwner,)

    def perform_create(self, serializer):
        serializer.save(session_key=self.request.session.session_key)

class CartDeleteAPIView(DestroyAPIView):
    permission_classes = (CartOwner,)

# @enable_session_key
# def cart_update(request, id=None):
#     cart = Cart.get(request.session, id)
#     if request.method == 'POST':
#         form = CartFormUpdate(request.POST, request=request, id=id)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             cart.update(name, description)
#             return redirect('carts:list')
#     else:
#         form = CartFormUpdate(instance=cart.cart, id=id)
#     context = {
#         'form': form
#     }
#     return render(request, 'update.html', context)

# @enable_session_key
# def cart_create(request):
#     if request.method == 'POST':
#         form = CartFormCreate(request.POST, request=request)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             Cart.add_new_cart(request.session, name, description)
#             return redirect('carts:list')
#     else:
#         form = CartFormCreate()
#     context = {
#         'form': form,
#     }
#     return render(request, 'create.html', context)

# @enable_session_key
# def cart_delete(request, id=None):
#     cart = Cart.get(request.session, id)
#     try:
#         cart.delete(request.session)
#     except CurrentCartCantBeDeleted as e:
#         raise Http404(str(e))
#     return redirect('carts:list')

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
