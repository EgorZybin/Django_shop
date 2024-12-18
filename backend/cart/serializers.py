from rest_framework import serializers
from cart.models import BasketItem
from product.serializers import ProductSerializer


class BasketItemSerializer(serializers.ModelSerializer):
    """
        Сериализатор для представления корзины и продуктов в ней
    """

    class Meta:
        model = BasketItem
        fields = ("product", "count")

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data["count"] = instance.count
        return data