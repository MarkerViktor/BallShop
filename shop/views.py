from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from order.models import Order, OrderStatus
from shop.models import Ball, Feedback, Manufacturer, Material, SportType


def index(request: HttpRequest):
    """Main page of the shop"""
    products = Ball.objects.all()
    return render(request, 'index.html', {'products': products})


def can_make_feedback(user: User, ball: Ball) -> bool:
    """Is user able to make a feedback for the ball?"""
    return Order.objects.filter(status=OrderStatus.wait_for_feedback, customer=user).filter(products__in=ball).count()


def can_user_make_feedback_to_product(user: User, product: Ball) -> bool:
    """Has user the order with status "wait_for_review" and the product?"""
    return Order.objects.filter(status=OrderStatus.wait_for_feedback.value, customer=user,
                                products__product=product).exists()


def ball_page(request: HttpRequest, ball_id: int):
    """Product-specific page view"""
    required_ball = get_object_or_404(Ball, id=ball_id)
    ball_feedbacks = Feedback.objects.filter(product=required_ball)
    can_feed = False
    if request.user.is_authenticated:
        can_feed = can_user_make_feedback_to_product(request.user, required_ball)

    return render(request, "product.html", {"product": required_ball,
                                            "can_feed": can_feed,
                                            "feedbacks": ball_feedbacks})


def search_form(request: HttpRequest):
    """Handle search query. Generate index page with required products"""
    query = str(request.GET.get("query", "")).strip()
    products = Ball.objects.filter(name__contains=query) | Ball.objects.filter(description__contains=query) | \
               Ball.objects.filter(name__contains=query.lower()) | Ball.objects.filter(description__contains=query.lower())
    return render(request, "index.html", {"products": products})


def specific_sport_filter_page(request: HttpRequest, sport_type_id: int):
    """Sport-specific catalog page view with filters"""

    selected_sport_type = SportType.objects.get(id=sport_type_id)

    # Get all product of selected category
    products = Ball.objects.filter(sport_type=selected_sport_type)
    products_prices = [product.price for product in products]

    # Calculate max and min price for selected category
    entered_max_price = request.GET.get("price_max")
    entered_min_price = request.GET.get("price_min")
    if entered_max_price is not None and entered_max_price != '':
        # if got max_price from form
        max_price = float(entered_max_price)
    else:
        max_price = max(products_prices)
    if entered_min_price is not None and entered_min_price != '':
        # if got max_price from form
        min_price = float(entered_min_price)
    else:
        min_price = min(products_prices)

    # Filter product py max and min price
    products = products.filter(price__gte=min_price, price__lte=max_price)

    all_manufacturers = Manufacturer.objects.all()
    all_materials = Material.objects.all()

    # Filter product by maker
    manufacturer = None
    if maker_id := request.GET.get("manufacturer"):
        products = products.filter(maker_id=maker_id)
        manufacturer = all_manufacturers.get(id=maker_id)

    # Filter product by material
    material = None
    if material_id := request.GET.get("material"):
        products = products.filter(material_id=material_id)
        material = all_materials.get(id=material_id)

    template_context = {
        "products": products,
        "sport_type": selected_sport_type,
        "category_id": sport_type_id,
        "manufacturers": Manufacturer.objects.all(),
        "materials": Material.objects.all(),
        "sel_manufacturer": manufacturer,
        "sel_material": material,
        "price_max": max_price,
        "price_min": min_price,
        "prices_max": max(products_prices),
        "prices_min": min(products_prices)
    }

    return render(request, "catalog.html", template_context)


def add_feedback_form(request: HttpRequest, ball_id: int):
    """Adding feedback to the ball"""
    user = request.user
    if user.is_authenticated:
        try:
            product = Ball.objects.get(id=ball_id)
        except Ball.DoesNotExist:
            # No ball with this id
            return HttpResponseRedirect('index_page')

        if can_user_make_feedback_to_product(user, product):
            text = request.POST.get('text')
            rate = request.POST.get('rate')

            new_feedback = Feedback(product=product,
                                    author=user,
                                    review_text=text,
                                    rate=rate,
                                    creation_datetime=datetime.now())
            new_feedback.save()

            return HttpResponseRedirect(reverse('product_page', args=[ball_id]))




