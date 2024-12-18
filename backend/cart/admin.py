from django.contrib import admin

# Register your models here.

from .models import Basket, BasketItem

admin.site.register(Basket)
admin.site.register(BasketItem)
