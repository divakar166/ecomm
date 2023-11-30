from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/<uid>/<quantity>/',checkout,name="checkout"),
    path('checkoutOrder/<uid>/',checkoutOrder,name='checkoutOrder'),
    path('removeCheckoutCoupon/',removeCheckoutCoupon,name='removeCheckoutCoupon'),
    path('removeAddressCheckout/<uid>/',removeAddressCheckout,name='removeAddressCheckout'),
    path('cartCheckout/',cartCheckout,name='cartCheckout'),
    path('removeCartCheckoutCoupon/',removeCartCheckoutCoupon,name='removeCartCheckoutCoupon')
]