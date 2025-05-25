from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_ID = models.CharField(max_length = 255, blank=True, null=True, unique=True)
    name = models.CharField(max_length = 255)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def get_absolute_url(self):
        return reverse('Product Detail', kwargs={'pk':self.pk})
    