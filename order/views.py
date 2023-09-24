from django.shortcuts import render
from products.models import Product,Coupon
from .models import CheckoutCart
from django.contrib import messages
from django.http import HttpResponseRedirect

def checkout(request,uid,quantity):
  product = Product.objects.get(uid=uid)
  try:
    checkout = CheckoutCart.objects.get(user=request.user)
    if checkout.product != product:
      checkout.product = product
      checkout.price = product.price
      checkout.quantity = quantity
    if request.method == 'POST':
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
    
    context = {'checkout':checkout}
    return render(request,'checkout/checkout.html',context=context)
  except Exception as e:
    print(e)
  try:
    checkout = CheckoutCart.objects.create(user=request.user,product=product,price=product.price,quantity=quantity)
    context = {'checkout':checkout}
    return render(request,'checkout/checkout.html',context=context)
  except Exception as e:
    print(e)

def removeCheckoutCoupon(request,uid):
  checkout = CheckoutCart.objects.get(uid=uid)
  checkout.coupon = None
  checkout.save()
  messages.warning(request, "Coupon Removed.")
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))