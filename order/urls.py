from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/<uid>/<quantity>/',checkout,name="checkout"),
    path('removeCheckoutCoupon/<uid>/',removeCheckoutCoupon,name='removeCheckoutCoupon')
]