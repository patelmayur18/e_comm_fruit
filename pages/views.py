from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import Disease,Product,CartItem,OrderItem,Address,Payment
from django.views.generic import TemplateView,DetailView,ListView,FormView
from django.core.paginator import Paginator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .forms import CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime
from django.views import generic
from django.conf import settings
# Create your views here.
# def index(request):

#     return render(request,'pages/index.html')

class DiseaseListView(LoginRequiredMixin,TemplateView):
    login_url="accounts/login/"
    template_name = 'pages/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseListView,self).get_context_data(*args,**kwargs)
        context['Disease'] = Disease.objects.all()
        return context


# def product(request,slug):
#     return render(request,'pages/shop.html')
@login_required(login_url="accounts/login/")
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

class ProductDetailView(LoginRequiredMixin,DetailView):
    login_url="accounts/login/"
    model = Product
    template_name =  'pages/shop-single.html' 

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        # d = Disease.objects.get(disease_slug = slug)
        # context['related_product'] = Product.objects.filter(disease=disease_slug)
        return context     

class cart(LoginRequiredMixin,View):
    login_url="accounts/login/"
    def get(self,*args,**kwargs):
        try:
            order = CartItem.objects.filter(user=self.request.user,ordered=False)
            total_order = OrderItem.objects.get(user=self.request.user,ordered=False)
            context ={
                'order':order,
                'total_order':total_order,
            }
            print(total_order.items.all())
            return render(self.request,'pages/shopping-cart.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"You Don't have any active order")
            return redirect('/')
       
@login_required(login_url="accounts/login/")
def about(request):
    return render(request,'pages/about-us.html') 

@login_required(login_url="accounts/login/")
def contact(request):
    return render(request,'pages/contact.html') 

class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'pages/checkout.html'
    form_class = CheckoutForm

    def form_valid(self, form):
        print("Hello")
        order = OrderItem.objects.get(user=self.request.user, ordered=False)
        print(order)
        selected_shipping_address = form.cleaned_data.get(
            'selected_shipping_address')
        selected_billing_address = form.cleaned_data.get(
            'selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='s',
                user=self.request.user,
                address_line_1=form.cleaned_data['shipping_address_line_1'],
                address_line_2=form.cleaned_data['shipping_address_line_2'],
                zip_code=form.cleaned_data['shipping_zip_code'],
                city=form.cleaned_data['shipping_city'],
                mobile_number=form.cleaned_data['shipping_mobile_number'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='b',
                user=self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                address_line_2=form.cleaned_data['billing_address_line_2'],
                zip_code=form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
                mobile_number=form.cleaned_data['billing_mobile_number'],
            )
            order.billing_address = address

        order.save()
        messages.info(self.request,
                      "You have successfully added your addresses")
        return super(CheckoutView, self).form_valid(form)

    def get_success_url(self):
        return reverse('payment_checkout')

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        print(kwargs["user_id"])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["order"] = OrderItem.objects.get(user=self.request.user,
                                             ordered=False)
        print(context["order"])
        return context

@login_required(login_url="accounts/login/")
def blog(request):
    return render(request,'pages/blog-single.html')   

@login_required(login_url="accounts/login/")
def add_to_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    cart_item,created = CartItem.objects.get_or_create(user=request.user,item=item)
    order_qs = OrderItem.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if item.stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
                messages.info(request,"The item quantity was updated")

                return redirect('cart')
            else:
                messages.info(request,"No more stock available")
                return redirect('cart')
        else:
            order.items.add(cart_item)
            messages.info(request,"This item was Added to your cart")
            return redirect('cart')
    else:
        orderd_date = timezone.now()
        order = OrderItem.objects.create(user=request.user,orderd_date = orderd_date)
        order.items.add(cart_item)
        messages.info(request,"This item was Added to your cart")
        return redirect('cart')

@login_required(login_url="accounts/login/")
def remove_single_from_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    cart_item,created = CartItem.objects.get_or_create(user=request.user,item=item)
    order_qs = OrderItem.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(user=request.user,item=item,ordered=False)[0]
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                order.items.remove(cart_item)
                cart_item.delete()

            messages.info(request,"The item quantity was updated")
            return redirect('cart')
        else:
            messages.info(request,"This item was not in your cart")
            return redirect('single_product',slug=slug)
    else:
        messages.info(request,"You don't have any active order")
        return redirect('single_product',slug=slug)    

            
@login_required(login_url="accounts/login/")
def remove_from_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs = OrderItem.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(user=request.user,item=item,ordered=False)[0]
            print(cart_item)
            order.items.remove(cart_item)
            cart_item.delete()
            messages.info(request,"The item was deleted")
            return redirect('cart')
        else:
            messages.info(request,"This item was not in your cart")
            return redirect('single_product',slug=slug)
    else:
        messages.info(request,"This item was not in your cart")
        return redirect('single_product',slug=slug)        



class ConfirmOrderView(LoginRequiredMixin, generic.View):


    def post(self, request, *args, **kwargs):
        order = OrderItem.objects.get(user=self.request.user, ordered=False)
        body = json.loads(request.body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='PayPal')
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})

    
class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["order"] = OrderItem.objects.get(user=self.request.user,
                                             ordered=False)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context["CALLBACK_URL"] = self.request.build_absolute_uri(
            reverse("thank"))
        # print(reverse("thank"))
        # print(self.request.build_absolute_uri(reverse("thank")))
        return context

class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/thank.html'        

   