from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import sendActivationEmail
from products.models import *


class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    isEmailVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.IntegerField(null=True)
    profile_image = models.ImageField(upload_to="profile",blank=True)
    gender = models.CharField(max_length=10,blank=True)

    def cartItemTotal(self):
        cart = Cart.objects.get(user=self.user,is_paid=False)
        return CartItems.objects.filter(cart=cart).count
    
class Address(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pincode = models.IntegerField()
    locality = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    landmark = models.CharField(max_length=50,null=True,blank=True)
    altMobile = models.IntegerField(null=True,blank=True)
    type = models.CharField(max_length=4)


class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)

    def cart_total(self):
        cart_items = CartItems.objects.filter(cart=self.uid)
        total = []
        for i in cart_items:
            total.append(int(i.quantity) * int(i.product.price))
        return sum(total)
    
    def finalTotal(self):
        total = self.cart_total()
        if self.coupon:
            return total - int(self.coupon.discount_price)
        return total


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartItems')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1,null=True)

class Wishlist(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product = models.ManyToManyField(Product,blank=True)



@receiver(post_save, sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance,emailToken=email_token)
            email = instance.email
            sendActivationEmail(email,email_token)
    except Exception as e:
        print(e)