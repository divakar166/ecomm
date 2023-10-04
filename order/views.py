from django.shortcuts import render
from products.models import Product,Coupon
from .models import CheckoutCart
from django.contrib import messages
from django.http import HttpResponseRedirect
from accounts.models import Address,Profile

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

  checkout = CheckoutCart.objects.get(user=request.user)
  checkout.product = product
  checkout.price = product.price
  checkout.quantity = quantity
  checkout.save()
  
  addressArray = Address.objects.filter(user=request.user)
  address = []
  for add in addressArray:
    address.append(add)
  print(checkout.address)
  context = {'checkout':checkout,'address':address,'userdata':userdata,'product':product}
  return render(request,'checkout/checkout.html',context=context)

def removeCheckoutCoupon(request,uid):
  checkout = CheckoutCart.objects.get(uid=uid)
  checkout.coupon = None
  checkout.save()
  messages.warning(request, "Coupon Removed.")
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def removeAddressCheckout(request,uid):
  checkout = CheckoutCart.objects.get(uid=uid)
  checkout.address = None
  checkout.save()
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))