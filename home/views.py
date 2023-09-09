from django.shortcuts import render
from products.models import Product
from accounts.models import Profile
# Create your views here.

def index(request):
    context = {'products':Product.objects.all()}
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        context['cartItemTotal'] = user.cartItemTotal()
    return render(request,'home/index.html',context)