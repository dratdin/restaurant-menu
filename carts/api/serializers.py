from rest_framework.serializers import ModelSerializer

from carts.models import Cart

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id',
            'name',
            'description'
        ]
