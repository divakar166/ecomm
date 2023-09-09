from django.shortcuts import render
from products.models import Product
from accounts.models import Profile
from accounts.views import addToCart,isItemInWishlist
# Create your views here.

def getProducts(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product':product}
        if request.method=='POST':
            quantity = request.POST.get('quantity')
            addToCart(request,product.uid,quantity)
        if request.user.is_authenticated: 
            context['wishlist'] = isItemInWishlist(request,product.uid)
            user = Profile.objects.get(user=request.user)
            context['cartItemTotal'] = user.cartItemTotal()
        return render(request,'product/product.html',context)
    except Exception as e:
        print(e)