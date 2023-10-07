from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from accounts.models import Coupon,Address
from products.models import Product
import ast

# class Order(BaseModel):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='order')
#     product = models.ManyToManyField(Product,null=True,blank=True)
#     coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
#     address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
#     amount = models.IntegerField(blank=True,null=True)
#     is_success = models.BooleanField(default=False)

class CartCheckout(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cartCheckout')
    product = models.ManyToManyField(Product,blank=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    amount = models.IntegerField(blank=True,null=True)
    quantity = models.CharField(max_length=500,blank=True,null=True)

    def total(self):
        total = 0
        quantity = self.quantity
        for x in self.product.all():
            for i in quantity:
                if x==i:
                    total += int(int(x.price)*int(quantity[i]))
        return total

    def final_total(self):
        value = self.total()
        if self.coupon:
            return value - int(self.coupon.discount_price)
        return value



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