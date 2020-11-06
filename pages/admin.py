from django.contrib import admin
from .models import Disease,Product,Address,CartItem,OrderItem,Payment
# Register your models here.
admin.site.register(Disease)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Payment)