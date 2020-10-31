from django.shortcuts import render
from .models import Disease,Product
from django.views.generic import TemplateView,DetailView,ListView
from django.core.paginator import Paginator
# Create your views here.
# def index(request):

#     return render(request,'pages/index.html')
class DiseaseListView(TemplateView):
    template_name = 'pages/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseListView,self).get_context_data(*args,**kwargs)
        context['Disease'] = Disease.objects.all()
        return context


# def product(request,slug):
#     return render(request,'pages/shop.html')

def ProductListView(request,slug):
    d = Disease.objects.get(disease_slug = slug )
    Products = Product.objects.filter(disease__in = [d])
    paginator = Paginator(Products,4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'Products':paged_products,
    }
    return render(request,'pages/shop.html',context)    

# def single_product(request,slug):
#     return render(request,'pages/shop-single.html')

class ProductDetailView(DetailView):
    model = Product
    template_name =  'pages/shop-single.html'      

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
