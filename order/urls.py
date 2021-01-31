from django.urls import path, include
from order import views

urlpatterns = [
    path("check/<int:order_id>", views.check_order_page, name="check_order_page"),
    path("cart/", views.cart_page, name="cart_page"),
    path("cart/clean", views.cart_clean_form, name="cart_clean_form"),
    path("cart/confirm", views.cart_confirm_form, name="cart_confirm_form"),
    path("cart/add/<int:ball_id>", views.cart_add_product_form, name="cart_add_product_form"),
]