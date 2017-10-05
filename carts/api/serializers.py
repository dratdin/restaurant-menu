from rest_framework.serializers import (
    Serializer,
    IntegerField,
    ModelSerializer, 
    StringRelatedField
)

from dishes.models import Dish
from carts.models import Cart, Item

from rest_framework.validators import UniqueTogetherValidator

class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'description'
        )

class CartItemSerializer(ModelSerializer):
    dish = DishSerializer(read_only=True)
    class Meta:
        model = Item
        fields = (
            'unit_price',
            'quantity',
            'dish',
            'total_price'
        )

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'pk',
            'name',
            'description',
            'count',
            'summary',
        )

class CartListSerializer(Serializer):
    carts = CartSerializer(many=True)
    current_cart_pk = IntegerField()

class CartDetailSerializer(ModelSerializer):
    item_set = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = (
            'pk',
            'name',
            'description',
            'count',
            'summary',
            'item_set'
        )

class CartCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'name',
            'description',
        )
        read_only_fields = ('pk',)