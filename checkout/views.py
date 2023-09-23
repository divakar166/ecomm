from django.shortcuts import render
from products.models import Product
from checkout.models import CheckoutCart
# Create your views here.
def checkout(request,uid):
  product = Product.objects.get(uid=uid)
  try:
    checkout_obj = CheckoutCart.objects.get(user=request.user)
    context = {'product':product,'checkout':checkout_obj}
    return render(request,'checkout/checkout.html',context=context)
  except Exception as e:
    print(e)
  checkout_obj = CheckoutCart.objects.create(user=request.user,product=product,price=product.price)
  checkout_obj.save()
  print(checkout_obj)
  context = {'product':product,'checkout':checkout_obj}
  return render(request,'checkout/checkout.html',context=context)