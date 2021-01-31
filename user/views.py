from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from order.models import Order


def registration_page(request: HttpRequest):
    """Registration page view"""
    return render(request, 'registration.html')


def registration_form(request: HttpRequest):
    """
    Registration form handler.
    If data of new user is valid he will be created and saved to db.
    """
    if request.method == "POST":
        # Try to extract new user data
        try:
            login_ = request.POST['login']
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            # Bad request
            return HttpResponse(status=400)

        # Try to creat new user
        try:
            new_user = User.objects.create_user(login_, email, password)
        except ValueError:
            return HttpResponse(status=400)

        login(request, new_user)
    return HttpResponseRedirect("/")


def login_form(request: HttpRequest):
    """
    User login for handler.
    If login and password are valid, the user will be authorized.
    """
    if request.method == "POST":
        form_username = request.POST.get('username')
        form_password = request.POST.get('password')

        user = User.objects.get(username=form_username)
        if user.check_password(form_password):
            login(request, user)
        else:
            return HttpResponse(status=400)

    path_to_redirect = request.POST.get('path_to_redirect', '/')
    return HttpResponseRedirect(path_to_redirect)


def logout_(request: HttpRequest):
    """Close user session, de-auth"""
    if request.user.is_authenticated:
        logout(request)
    path_to_redirect = request.GET.get('path', '/')
    return HttpResponseRedirect(path_to_redirect)


def user_profile_page(request: HttpRequest):
    """User profile page view"""
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(customer=request.user)
        return render(request, 'user_profile.html', {'orders': user_orders})
    else:
        return HttpResponseRedirect(reverse('index_page'))


def user_edit_profile_page(request: HttpRequest):
    """Page with form to edit user personal information"""
    return render(request, 'user_profile_edit_page.html')


def user_edit_profile_form(request: HttpRequest):
    """Edit user profile information"""
    user = request.user
    if user.is_authenticated:
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        user.email = new_email
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(reverse('user_profile_page'))
    else:
        return HttpResponseRedirect(reverse('index_page'))

