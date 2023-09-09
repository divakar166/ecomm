from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self)->str:
        return self.category_name



class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="product")
    price = models.IntegerField()
    model = models.CharField(max_length=20,default='NAN')
    product_desc = models.TextField()
    image = models.ImageField(upload_to='product')

    def save(self,*args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)

    def __str__(self)->str:
        return self.product_name
    
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amt = models.IntegerField(default=500)