from django.contrib import admin
from .models import Product, Review, ProductImage, Specifications, Sale


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели Товара"""

    inlines = [
        ProductInline,
    ]

    list_display = [
        "id",
        "title",
        "price",
        "salePrice",
        "count",
        "category",
        "freeDelivery",
        "limited_edition",
        "sorted_index",
        "rating",
    ]
    list_filter = [
        "price",
        "category",
        "freeDelivery",
        "limited_edition",
        "sorted_index",
    ]
    search_fields = ["title", "id"]

    def rating(self, obj):
        return obj.rating  # достаём рейтинг объекта

    def salePrice(self, obj) -> float:
        try:
            return obj.sale_products.salePrice  # Получаем существующую скидку на объект
        except Exception:
            return float(obj.price)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация модели отзывов"""

    list_display = ["author", "email", "rate", "date", "updated"]
    list_filter = ["rate", "date", "updated"]
    search_fields = ["author", "email"]


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    """Регистрация спецификации товара"""

    list_display = ["name", "value", "product"]
    search_fields = ["name"]
    list_filter = ["product"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Регистрация Скидки товара"""

    list_display = ["product", "sale", "dateTo", "dateFrom", "salePrice"]
    list_filter = ["sale", "dateTo", "dateFrom"]
    search_fields = ["sale", "product"]

    def SalePrice(self, obj) -> float:
        return obj.salePrice  # Достаём скидку товара в %
