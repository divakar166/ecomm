from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from .models import Profile
from products.models import *
from accounts.models import Cart,CartItems,Wishlist,Address
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get("email")
            password = request.POST.get("password")

            user_obj = User.objects.filter(username=email)
            if not user_obj.exists():
                messages.warning(request,'Account not found.')
                return HttpResponseRedirect(request.path_info)
            
            if not user_obj[0].profile.isEmailVerified:
                messages.warning(request,'Your account is not verified.')
                return HttpResponseRedirect(request.path_info)

            user_obj = authenticate(username=email,password=password)
            if user_obj:
                login(request,user_obj)
                return redirect('/')
            
            messages.warning(request,'Invalid credentials.')
            return HttpResponseRedirect(request.path_info)
        
        return render(request,'accounts/login.html')
    return redirect('/')


def register_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            email = request.POST.get("email")
            password = request.POST.get("password")

            user_obj = User.objects.filter(username=email)
            if user_obj.exists():
                messages.warning(request,'Email is already taken.')
                return HttpResponseRedirect(request.path_info)
            user_obj = User.objects.create(first_name=firstName,last_name=lastName,email=email,username=email)
            user_obj.set_password(password)
            user_obj.save()
            Wishlist.objects.create(user=user_obj)
            Cart.objects.create(user=user_obj,is_paid=False)
            messages.success(request,'An email has been sent on your mail.')
            return HttpResponseRedirect(request.path_info)

        return render(request,'accounts/register.html')
    return redirect('/')


def activate_email(request,email_token):
    try:
        user = Profile.objects.get(emailToken=email_token)
        user.isEmailVerified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid token!')

@login_required(login_url="/accounts/login/")
def addToCart(request,uid,quantity):
    product = Product.objects.get(uid=uid)
    user = request.user
    cart,_ = Cart.objects.get_or_create(user=user,is_paid=False)
    try:
        cart_item = CartItems.objects.get(cart=cart,product=product)
        if cart_item:
            cart_item.quantity += int(quantity)
            cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
    cart_item = CartItems.objects.create(cart=cart,product=product,quantity=quantity)
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request,cart_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def cart(request):
    cart = Cart.objects.get(user=request.user,is_paid=False)
    cartitems = CartItems.objects.filter(cart=cart)
    context = {'cart':cart,'cartitems':cartitems}
    user = Profile.objects.get(user=request.user)
    context['cartItemTotal'] = user.cartItemTotal()
    if cart.coupon:
        coupon_obj = Coupon.objects.get(coupon_code=cart.coupon.coupon_code)
        if cart.cart_total() < coupon_obj.minimum_amt:
            cart.coupon = None
            cart.save()

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
        if not coupon_obj:
            messages.warning(request,'Invalid Coupon Code.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.coupon:
            messages.warning(request,'Coupon already applied.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.cart_total() < coupon_obj[0].minimum_amt:
            messages.warning(request,f'Amount must be greater than {coupon_obj[0].minimum_amt}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_obj[0].is_expired:
            messages.warning(request,'Coupon expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request,'Applied Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'accounts/cart.html',context=context)

def updateCart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        uid = request.POST.get('cartItemID')
        cart_item = CartItems.objects.get(uid=uid)
        cart_item.quantity = quantity
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def removeCoupon(request,uid):
    cart = Cart.objects.get(uid=uid)
    cart.coupon = None
    cart.save()
    messages.warning(request,'Coupon Removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def myaccount(request):
    return render(request,'accounts/myaccount.html')

def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    product = []
    for wish in wishlist:
        products = wish.product.all()
        for x  in products:
            product.append(x)
    context = {'products':product}
    user = Profile.objects.get(user=request.user)
    context['cartItemTotal'] = user.cartItemTotal()
    return render(request,'accounts/wishlist.html',context=context)

def wishlistRemove(request,uid):
    user = request.user
    wishlist = Wishlist.objects.get(user=user)
    wishlist.product.remove(uid)
    wishlist.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def isItemInWishlist(request,uid):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    for wish in wishlist:
        product = wish.product.all()
        for x in product:
            if x.uid == uid:
                return True
    return False

def addItemInWishlist(request,uid):
    user = request.user
    wishlist = Wishlist.objects.get(user=user)
    wishlist.product.add(Product.objects.get(uid=uid))
    wishlist.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def address(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        locality = request.POST.get('locality')
        area = request.POST.get('area')
        city = request.POST.get('city')
        state = request.POST.get('state')
        landmark = request.POST.get('landmark')
        alt_mobile = request.POST.get('alt_mobile')
        if alt_mobile == '':
            alt_mobile = None
        type = request.POST.get('type')
        try:
            new_add = Address.objects.create(user=user,
                                             name=name,
                                             mobile=mobile,
                                             pincode=pincode,
                                             locality=locality,
                                             area=area,
                                             city=city,
                                             state=state,
                                             landmark=landmark,
                                             altMobile=alt_mobile,
                                             type=type)
            new_add.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            return e
    addressArray = Address.objects.filter(user=user)
    address = []
    for add in addressArray:
        address.append(add)
    context = {'address':address,'count':addressArray.count()}
    user = Profile.objects.get(user=user)
    context['cartItemTotal'] = user.cartItemTotal()
    return render(request,'accounts/address.html',context=context)

def deleteAddress(request,uid):
    address = Address.objects.get(uid=uid)
    address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def fetchAddress(request,uid):
    address = Address.objects.get(uid=uid)
    add = {'name':address.name,
           'mobile':address.mobile,
           'pincode':address.pincode,
           'locality':address.locality,
           'area':address.area,
           'city':address.city,
           'state':address.state,
           'landmark':address.landmark,
           'alt_mobile':address.altMobile,
           'type':address.type}
    return JsonResponse({"data":add},status=200)

def editAddress(request,*args,**kwargs):
    if request.method == 'POST':
        name = request.POST.get('edit_name')
        print(name)
        return 'nunnu'

def profile(request):
    user = request.user
    userData = Profile.objects.get(user=request.user)
    context = {'userData':userData}  
    context['cartItemTotal'] = userData.cartItemTotal()
    return render(request,'accounts/profile.html',context=context)

def orders(request):
    user = request.user
    context = {'user':request.user}
    user = Profile.objects.get(user=request.user)
    context['cartItemTotal'] = user.cartItemTotal()
    return render(request,'accounts/orders.html',context=context)

def logout(request):
    return HttpResponse('Logging Out!')