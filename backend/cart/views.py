from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import BasketItem
from cart.serializers import BasketItemSerializer
from cart.models import Basket
from product.models import Product


class BasketAPIView(APIView):
    def get(self, request):
        """
            Вывод информации о товарах в корзине
        """
        queryset = BasketItem.objects.filter(basket__user=request.user).select_related('product')
        serializer = BasketItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        id = request.data['id']
        count = request.data['count']
        basket, created = Basket.objects.update_or_create(user=request.user)
        product = Product.objects.get(id=id)
        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
        basket_item.count = count
        basket_item.save()
        basket_items = BasketItem.objects.filter(basket=basket).select_related('product')
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=201)

    def delete(self, request):
        id = request.data['id']
        count = request.data['count']
        basket = request.user.basket
        product = Product.objects.get(id=id)
        basket_item = BasketItem.objects.select_related('product').get(basket=basket, product=product)
        if basket_item.count > count:
            basket_item.count -= count
            basket_item.save()
        else:
            basket_item.delete()
        basket_items = BasketItem.objects.filter(basket=basket).select_related('product')
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data)
