from django.urls import path, include
from shop import views

urlpatterns = [
    path("ball/<int:ball_id>/", views.ball_page, name="product_page"),
    path("ball/<int:ball_id>/add_feedback", views.add_feedback_form, name="add_feedback"),
    path("sport/<int:sport_type_id>/", views.specific_sport_filter_page, name="catalog"),
    path("search/", views.search_form, name="search_form"),
]
