from django.contrib import admin
from .models import Profile,Cart,CartItems,Wishlist,Address

# Register your models here.
admin.site.register(Profile)

admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Wishlist)
admin.site.register(Address)