from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:server_id>/', views.add_cart, name='add_cart'),
    path('add_no_dupe/<int:server_id>/', views.add_no_dupe, name='add_no_dupe'),
    path('add_rental_extension/<rental_id>/', views.add_rental_extension_cart, name="add_rental_extension"),
    path('remove_cart/<str:secondary_id>', views.remove_cart, name='remove_cart'),
    path('remove_cart_extension/<rental_id>', views.remove_cart_extension, name='remove_cart_extension'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('payments/', views.payment_detail, name='payment_detail'),
    path('payments/checkout', views.checkout, name='checkout')
]
