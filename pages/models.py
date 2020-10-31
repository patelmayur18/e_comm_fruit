from django.db import models
from django.shortcuts import reverse
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