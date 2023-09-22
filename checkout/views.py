from django.shortcuts import render

# Create your views here.
def checkout(request,uid):
  print(uid)
  return render(request,'checkout/checkout.html')