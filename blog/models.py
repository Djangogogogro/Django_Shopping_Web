from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_ID = models.IntegerField()
    name = models.CharField(max_length = 255)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def get_absolute_url(self):
        return reverse('Product Detail', kwargs={'pk':self.pk})

class User(models.Model):
    user_ID = models.IntegerField()
    user_mail = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 255)
    user_password = models.CharField(max_length = 255) #Hash

class Customer(User):
    address = models.CharField(blank=True, max_length = 255)

class Shopping_Cart(models.Model):
    user_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)

class Seller(User):
    products = models.ManyToManyField(Product, blank=True)
    rating = models.FloatField(default=0.0)

class Order(models.Model):
    order_ID = models.IntegerField()
    products = models.ManyToManyField(Shopping_Cart, blank=True)
    customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    seller_ID = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True)
    