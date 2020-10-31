from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'pages/index.html')


def product(request):
    return render(request,'pages/shop.html')

def single_product(request):
    return render(request,'pages/shop-single.html')    

def cart(request):
    return render(request,'pages/shopping-cart.html')   

def about(request):
    return render(request,'pages/about-us.html') 

def contact(request):
    return render(request,'pages/contact.html') 

def checkout(request):
    return render(request,'pages/checkout.html')    

def login(request):
    return render(request,'pages/login.html')    

def register(request):
    return render(request,'pages/register.html')   

def blog(request):
    return render(request,'pages/blog-single.html')                             
