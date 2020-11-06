from django.urls import path
from .views import cart,about,contact,CheckoutView,blog,DiseaseListView,ProductListView,ProductDetailView,add_to_cart,remove_single_from_cart,remove_from_cart,PaymentView,ConfirmOrderView,ThankYouView
urlpatterns = [
    path('',DiseaseListView.as_view(),name='home'),
    path('shop/<slug>',ProductListView,name='shop'),
    path('single-product/<slug>',ProductDetailView.as_view(),name='single_product'),
    path('cart',cart.as_view(),name='cart'),
    path('add-to-cart/<slug>',add_to_cart,name='add_to_cart'),
    path('remove_single_from_cart/<slug>',remove_single_from_cart,name='remove_single_from_cart'),
    path('remove_from_cart/<slug>',remove_from_cart,name='remove_from_cart'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
    path('checkout',CheckoutView.as_view(),name='checkout'),
    path('blog',blog,name='blog'),
    path('payment',PaymentView.as_view(),name='payment_checkout'),
    path('ConfirmOrderView',ConfirmOrderView.as_view(),name='confirm-order'),
    path('ThankYouView',ThankYouView.as_view(),name='thank'),
]
