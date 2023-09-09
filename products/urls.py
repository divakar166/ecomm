from django.urls import path
from products.views import getProducts

urlpatterns = [
    path('<slug>/',getProducts,name="getProduct")
]