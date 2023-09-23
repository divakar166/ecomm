from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from accounts.models import Coupon
from products.models import Product
# Create your models here.
class CheckoutCart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='checkout')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    price = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)
