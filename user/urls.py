from django.urls import path
from django.views.generic import TemplateView

from user import views


urlpatterns = [
    path('registration/', views.registration_page, name='registration_page'),
    path('registration', views.registration_form, name='registration_form'),
    path('login', views.login_form, name='login_form'),
    path('logout', views.logout_, name='logout'),
    path('profile/', views.user_profile_page, name='user_profile_page'),
    path('profile/edit/', views.user_edit_profile_page, name='user_edit_profile_page'),
    path('profile/edit', views.user_edit_profile_form, name='user_edit_profile_form')
]
