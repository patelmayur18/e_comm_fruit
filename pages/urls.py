from django.urls import path
from .views import index,product,single_product,cart,about,contact,checkout,login,register,blog
urlpatterns = [
    path('',index,name='home'),
    path('product',product,name='product'),
    path('single-product',single_product,name='single_product'),
    path('cart',cart,name='cart'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
    path('checkout',checkout,name='checkout'),
    path('login',login,name='login'),
    path('register',register,name='register'),
    path('blog',blog,name='blog'),
]
