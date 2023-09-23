from django.urls import path
from checkout.views import *

urlpatterns = [
    path('<uid>/',checkout,name="checkout")
]