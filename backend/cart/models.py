from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.http import HttpRequest
from product.models import Product


class Basket(models.Model):
    """
        Модель корзины, связанная с пользователем,
        имеющая дату её создания
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __init__(self, request: HttpRequest, *args, **kwargs):
        """Инициализация корзины при помощи django-session"""

        super().__init__(*args, **kwargs)
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)  # Достаём существующую сессию
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # Создаём новую сессию
        self.cart = cart  # Оставляем текущую сессию

    def clear(self) -> None:
        """Метод для очищения корзины"""

        del self.session[settings.CART_SESSION_ID]  # Удаляем текущую сессию
        self.save()


class BasketItem(models.Model):
    """
        Модель корзины с товарами, имеющая какое-то кол-во товаров,
        по умолчанию 1 товар
    """

    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, verbose_name="Корзина",
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Продукт",
    )
    count = models.PositiveIntegerField(
        default=1, verbose_name="Кол-во"
    )
