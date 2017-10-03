from rest_framework.serializers import ModelSerializer, StringRelatedField

from dishes.models import Dish
from carts.models import Cart, Item

class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'id',
            'name',
            'description'
        ] 

class CartItemSerializer(ModelSerializer):
    dish = DishSerializer(read_only=True)
    class Meta:
        model = Item
        fields = [
            'unit_price',
            'quantity',
            'dish',
            'total_price'
        ]

class CartListSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'pk',
            'name',
            'description',
            'count',
            'summary',
        ]

class CartDetailSerializer(ModelSerializer):
    item_set = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = [
            'pk',
            'name',
            'description',
            'count',
            'summary',
            'item_set'
        ]

class CartCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'name',
            'description',
        ]