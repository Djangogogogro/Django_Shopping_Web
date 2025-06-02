from django.db import models
from django.urls import reverse
from showitem.models import (
    Product
)

class User(models.Model):
    user_ID = models.CharField(max_length = 255)
    user_mail = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 255)
    user_password = models.CharField(max_length = 255) #Hash

class Customer(User):
    address = models.CharField(blank=True, max_length = 255)

class Shopping_Cart(models.Model):
    user_ID = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)

class Seller(User):
    products = models.ManyToManyField(Product, blank=True)
    rating = models.FloatField(default=0.0)

class Order(models.Model):
    order_ID = models.CharField(max_length = 255)
    products = models.CharField(max_length = 1024, blank=True)
    customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    seller_ID = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    