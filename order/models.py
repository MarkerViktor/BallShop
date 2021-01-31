from datetime import datetime
from enum import Enum

from django.contrib.auth.models import User
from django.db import models

from shop.models import Ball


class ProductInCart(models.Model):
    product = models.ForeignKey(Ball, on_delete=models.CASCADE,
                                verbose_name='Specific product added to the card',)
    quantity = models.IntegerField(verbose_name='Quantity of specific products added to card')

    def __str__(self):
        return f"{self.id}: {self.product.name} (× {self.quantity})"


class ShoppingCart(models.Model):
    """Consist some selected by user products"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInCart, verbose_name='List of selected products')

    @property
    def total_cost(self):
        sum_cost = 0
        for product_in_cart in self.products.all():
            sum_cost += product_in_cart.product.price * product_in_cart.quantity
        return sum_cost


class DeliveryAddress(models.Model):
    """An address whither the order will be delivered"""
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=20)
    office = models.CharField(max_length=20)

    def __str__(self):
        return f"г. {self.city}, ул. {self.street}, д. {self.house}, кв. {self.office}"


class PaymentMethod(models.Model):
    """Possible payment methods"""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class OrderStatus(Enum):
    """Possible order statuses"""
    new = 0
    wait_for_payment = 1
    wait_for_delivery = 2
    wait_for_feedback = 3
    complete = 4


class Order(models.Model):
    """Confirmed order of several products"""
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInCart, verbose_name='List of purchased products')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)
    status = models.IntegerField(verbose_name='Condition of the order. See «OrderStatus» enum')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    creation_datetime = models.DateTimeField()

    @property
    def total_cost(self):
        sum_cost = 0
        for product_in_cart in self.products.all():
            sum_cost += product_in_cart.product.price * product_in_cart.quantity
        return sum_cost

    def get_status(self, new_status: OrderStatus):
        """Edit order status"""
        self.status = new_status
        self.save()

    @property
    def status_str(self):
        return OrderStatus(self.status).name

    def __str__(self):
        return f"№ {self.id} от {self.creation_datetime}"