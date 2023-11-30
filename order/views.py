from django.shortcuts import render
from products.models import Product,Coupon
from .models import CheckoutCart,CartCheckout
from django.contrib import messages
from django.http import HttpResponseRedirect
from accounts.models import Address,Profile,Cart,CartItems
from django.contrib.auth.decorators import login_required

# Checkout Views

@login_required(login_url="/accounts/login/")
def checkout(request,uid,quantity):
  product = Product.objects.get(uid=uid)
  userdata = Profile.objects.get(user=request.user)

  if request.method == 'POST':
    checkout = CheckoutCart.objects.get(user=request.user)
    if request.POST.get('coupon'):
      coupon = request.POST.get('coupon')
      coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
      if not coupon_obj:
        messages.warning(request, "Invalid Coupon Code.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if checkout.coupon:
        messages.warning(request, "Coupon already applied.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if checkout.checkout_total() < coupon_obj[0].minimum_amt:
        messages.warning(
          request, f"Amount must be greater than {coupon_obj[0].minimum_amt}"
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if coupon_obj[0].is_expired:
        messages.warning(request, "Coupon expired.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      checkout.coupon = coupon_obj[0]
      checkout.save()
      messages.success(request, "Applied Successfully!")
      return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if request.POST.get('address'):
      add = request.POST.get('address')
      checkout.address = Address.objects.get(uid=add)
      checkout.save()
      return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
  addressArray = Address.objects.filter(user=request.user)
  address = []
  for add in addressArray:
    address.append(add)
  try:
    checkout = CheckoutCart.objects.get_or_create(user=request.user,product=product)
    checkout[0].price = product.price
    checkout[0].quantity = quantity
    checkout[0].save()
    context = {'checkout':checkout[0],'address':address,'userdata':userdata,'product':product}
    return render(request,'checkout/checkout.html',context=context)
  except Exception as e:
    print(e)
    
  checkout = CheckoutCart.objects.get(user=request.user)
  checkout.product = product
  checkout.price = product.price
  checkout.quantity = quantity
  checkout.save()
  
  context = {'checkout':checkout,'address':address,'userdata':userdata,'product':product}
  return render(request,'checkout/checkout.html',context=context)

def removeCheckoutCoupon(request):
  checkout = CheckoutCart.objects.get(user=request.user)
  checkout.coupon = None
  checkout.save()
  messages.warning(request, "Coupon Removed.")
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def removeAddressCheckout(request,uid):
  checkout = CheckoutCart.objects.get(uid=uid)
  checkout.address = None
  checkout.save()
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# Checkout from Cart Views

def cartCheckout(request):
  userData = Profile.objects.get(user=request.user)
  cart = Cart.objects.get(user=request.user)
  items = CartItems.objects.filter(cart=cart)
  cartCheckout = CartCheckout.objects.get(user=request.user)
  dict = {}
  for x in items:
    cartCheckout.product.add(x.product)
    dict[x.product] = x.quantity
  cartCheckout.quantity = dict
  cartCheckout.coupon = cart.coupon
  cartCheckout.save()
  if request.method == 'POST':
    if request.POST.get('coupon'):
      coupon = request.POST.get('coupon')
      coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
      if not coupon_obj:
        messages.warning(request, "Invalid Coupon Code.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if cartCheckout.coupon:
        messages.warning(request, "Coupon already applied.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if cartCheckout.total() < coupon_obj[0].minimum_amt:
        messages.warning(
          request, f"Amount must be greater than {coupon_obj[0].minimum_amt}"
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      if coupon_obj[0].is_expired:
        messages.warning(request, "Coupon expired.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
      cartCheckout.coupon = coupon_obj[0]
      cartCheckout.save()
      messages.success(request, "Applied Successfully!")
      return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if request.POST.get('address'):
      add = request.POST.get('address')
      cartCheckout.address = Address.objects.get(uid=add)
      cartCheckout.save()
      return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
  addressArray = Address.objects.filter(user=request.user)
  address = []
  for add in addressArray:
    address.append(add)
  context = {'cartCheckout':cartCheckout,'dict':dict,'userdata':userData,'address':address}
  return render(request,'checkout/cartCheckout.html',context=context)

def removeCartCheckoutCoupon(request):
  checkout = Cart.objects.get(user=request.user)
  checkout.coupon = None
  checkout.save()
  messages.warning(request, "Coupon Removed.")
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def checkoutOrder(request,uid):
  return render(request,'checkout/payment.html')