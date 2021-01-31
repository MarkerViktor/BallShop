from datetime import datetime

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from order.models import Order, OrderStatus, ShoppingCart, PaymentMethod, ProductInCart, DeliveryAddress
from shop.models import Ball


def check_order_page(request: HttpRequest, order_id: int):
    """Page showing the the status of order"""
    selected_order = Order.objects.get(id=order_id)
    order_status = OrderStatus(selected_order.status).name
    return render(request, 'order.html', {'order': selected_order})


def cart_page(request: HttpRequest, form_error=False):
    """Page showing products which in the user's cart now"""
    user = request.user
    if user.is_authenticated:
        try:
            cart = ShoppingCart.objects.get(owner=user)
        except ShoppingCart.DoesNotExist:
            cart = None
        payment_methods = PaymentMethod.objects.all()
        addresses = DeliveryAddress.objects.all()
        return render(request, "cart_page.html", {"cart": cart,
                                                  "payment_methods": payment_methods,
                                                  "addresses": addresses,
                                                  "form_error": form_error})
    else:
        return HttpResponseRedirect(reverse('index_page'))


def cart_clean_form(request: HttpRequest):
    """Clear shopping cart of the user"""
    user = request.user
    try:
        cart = ShoppingCart.objects.get(owner=user)
        cart.delete()
    except ShoppingCart.DoesNotExist:
        pass
    return HttpResponseRedirect('/')


def cart_add_product_form(request: HttpRequest, ball_id: int):
    """Add selected product to active user shopping cart"""
    user = request.user
    if user.is_authenticated:
        # Get ball by id
        added_product = Ball.objects.get(id=ball_id)

        # Get or create cart object
        try:
            cart = ShoppingCart.objects.get(owner=user)
        except ShoppingCart.DoesNotExist:
            cart = ShoppingCart(owner=user)
            cart.save()

        # Add product to cart
        if not cart.products.filter(product=added_product).exists():
            # Add ProductInCart if this product is not in cart
            cart.products.create(product=added_product, quantity=1)
        else:
            # Increment quantity ff this product is in cart
            product_in_cart = cart.products.get(product=added_product)
            product_in_cart.quantity += 1
            product_in_cart.save()

        path_to_redirect = request.GET.get("path_to_redirect", '/')
        return HttpResponseRedirect(path_to_redirect)
    else:
        return HttpResponseRedirect(reverse('index_page'))


def cart_confirm_form(request: HttpRequest):
    """Confirm an order form"""
    user = request.user
    if user.is_authenticated:
        address_id = request.POST.get('address')
        payment_method_id = request.POST.get('payment_method')

        try:
            cart = ShoppingCart.objects.get(owner=user)
            address = DeliveryAddress.objects.get(id=address_id)
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
        except ShoppingCart.DoesNotExist:
            # If user hasn't shopping cart, he cannot make order
            return HttpResponseRedirect(reverse('index_page'))
        except DeliveryAddress.DoesNotExist:
            # Bad address
            return cart_page(request, True)
        except PaymentMethod.DoesNotExist:
            # Bad payment_method
            return cart_page(request, True)

        new_order = Order(
            customer=user,
            address=address,
            status=0,  # «new»
            payment_method=payment_method,
            creation_datetime=datetime.now(),
        )
        new_order.save()

        # Add products from cart to order
        for product_in_cart in cart.products.all():
            new_order.products.add(product_in_cart)
        new_order.save()

        # Clear cart by redirected
        return HttpResponseRedirect(reverse('cart_clean_form'))
    else:
        return HttpResponseRedirect(reverse('index_page'))


