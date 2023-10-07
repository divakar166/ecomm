from django.shortcuts import render,redirect
from products.models import Product
from accounts.models import Profile
from accounts.views import addToCart,isItemInWishlist
from django.http import HttpResponseRedirect
from order.views import checkout

def getProducts(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product':product}
        if request.method=='POST':
            buy = request.POST.get('buy')
            quantity = request.POST.get('quantity')
            if buy=='True':
                return redirect('checkout',uid=product.uid,quantity=quantity)
            else:
                addToCart(request,product.uid,quantity)
        if request.user.is_authenticated: 
            context['wishlist'] = isItemInWishlist(request,product.uid)
            user = Profile.objects.get(user=request.user)
            context['cartItemTotal'] = user.cartItemTotal()
        return render(request,'product/product.html',context)
    except Exception as e:
        print(e)