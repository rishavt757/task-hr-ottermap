# shops/urls.py
from django.urls import path
from .views import register_shop, search_shops, register_shop_form, search_shops_form

urlpatterns = [
    path('register/', register_shop_form, name='register_shop_form'),  # for rendering form
    path('register/api/', register_shop, name='register_shop'),  # API for registration
    path('search/', search_shops_form, name='search_shops_form'),  # for rendering form
    path('search/api/', search_shops, name='search_shops'),  # API for search
]