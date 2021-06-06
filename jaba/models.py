from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.shortcuts import reverse
from django.db import models
from phonenumber_field import phonenumber
from phonenumber_field .modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.db.models.fields import BooleanField, DateField, DateTimeField, SlugField

#Location choices


# Create your models here.

class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_seller =  models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=15, unique=True)
    
    USERNAME_FIELD = 'phonenumber'
    
    def __str__(self):
        return self.username

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    locations = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_page", kwargs={'pk': self.pk})
    

class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender')


    def __str__(self):
        return self.sender