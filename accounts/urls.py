from django.urls import path
from accounts.views import *


urlpatterns = [
    path('login/',login_page,name="login"),
    path('register/',register_page,name='register'),
    path('activate/<email_token>/',activate_email,name='activate_email'),
    path('cart/',cart,name='cart'),
    path('remove_cart/<cart_uid>/',remove_cart,name='remove_cart'),
    path('addToCart/<uid>/',addToCart,name='addToCart'),
    path('removeCoupon/<uid>/',removeCoupon,name='removeCoupon'),
    path('updateCart/',updateCart,name='updateCart'),
    path('wishlist/',wishlist,name='wishlist'),
    path('wishItemRemove/<uid>/',wishlistRemove,name='wishlistRemove'),
    path('addItemInWishlist/<uid>/',addItemInWishlist,name='addItemInWishlist'),
    path('myaccount/',myaccount,name='myaccount'),
    path('address/',address,name='address'),
    path('profile/',profile,name='profile'),
    path('orders/',orders,name='orders'),
    path('logout/',logout,name='logout')
]