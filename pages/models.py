from django.db import models
from django.shortcuts import reverse
from django.conf import settings
# Create your models here.
class Disease(models.Model):
    disease_name = models.CharField(max_length=100)
    disease_photo = models.ImageField()
    disease_slug = models.SlugField()
    def get_absolute_url(self):
        return reverse('shop',kwargs={'slug':self.disease_slug})
    def __str__(self):
        return self.disease_name

class Product(models.Model):
    disease = models.ManyToManyField(Disease,blank=True)
    title = models.CharField(max_length=100)
    photo = models.ImageField()
    discription = models.TextField()
    slug = models.SlugField()
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('single_product',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def get_price(self): 
        return self.price   

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.item.title}"

    def get_cart_raw_total(self):
        return self.quantity * self.item.price    

class Address(models.Model):
    address_choice=(
        ('s','shipping'),
        ('b','billing'),
        )            
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=10,null=True,blank=True)
    address_type = models.CharField(choices=address_choice,max_length=1)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.zip_code}"

    class Meta:
        verbose_name_plural = 'Addresses'    


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    items = models.ManyToManyField(CartItem)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)    
    start_date = models.DateTimeField(auto_now_add=True)
    orderd_date = models.DateTimeField(blank=True,null=True)
    billing_address = models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True,related_name='billing_address')
    shipping_address = models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True,related_name='shipping_address')
    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def __str__(self):
        return self.reference_number

    def grand_total(self):
        Total = 0
        for price in self.items.all():
            Total += price.get_cart_raw_total()
        return Total        
   

   

class Payment(models.Model):
    order = models.ForeignKey(OrderItem,
                              on_delete=models.CASCADE,
                              related_name='payments')
    payment_method = models.CharField(max_length=20,
                                      choices=(('PayPal', 'PayPal'), ))
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def _str_(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"
    