from django.urls import path
from .views import cart,about,contact,checkout,login,register,blog,DiseaseListView,ProductListView,ProductDetailView
urlpatterns = [
    path('',DiseaseListView.as_view(),name='home'),
    path('shop/<slug>',ProductListView,name='shop'),
    path('single-product/<slug>',ProductDetailView.as_view(),name='single_product'),
    path('cart',cart,name='cart'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
    path('checkout',checkout,name='checkout'),
    path('login',login,name='login'),
    path('register',register,name='register'),
    path('blog',blog,name='blog'),
]
