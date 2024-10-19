from django.urls import path
from api.views import register_shop, search_shops, register_shop_form, search_shops_form, delete_shop, view_all_shops

urlpatterns = [
    path('register/', register_shop, name='register_shop'),
    path('search/', search_shops, name='search_shops'),
    path('shop/<int:shop_id>/delete/', delete_shop, name='delete_shop'),
    path('shops/', view_all_shops, name='view_all_shops'),

    
    path('', register_shop_form, name='register_shop_form'),
    path('search-form/', search_shops_form, name='search_shops_form'),
]