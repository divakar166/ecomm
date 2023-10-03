from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from accounts.models import Coupon,Address
from products.models import Product

class CheckoutCart(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='checkout')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    price = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)

    def checkout_total(self):
        return int(self.price)*int(self.quantity)

    def checkout_final_total(self):
        value = int(self.price) * int(self.quantity)
        if self.coupon:
            return value - int(self.coupon.discount_price)
        return value