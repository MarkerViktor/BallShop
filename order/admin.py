from django.contrib import admin
from order.models import *

# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(DeliveryAddress)
admin.site.register(PaymentMethod)
admin.site.register(Order)
admin.site.register(ProductInCart)
