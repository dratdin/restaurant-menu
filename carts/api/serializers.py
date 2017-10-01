from rest_framework.serializers import ModelSerializer, StringRelatedField

from carts.models import Cart, Item

class CartItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'unit_price',
            'quantity',
            'dish'
        ]

class CartListSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'name',
            'description',
            'count',
            'summary'
        ]

class CartDetailSerializer(ModelSerializer):
    item_set = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = [
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