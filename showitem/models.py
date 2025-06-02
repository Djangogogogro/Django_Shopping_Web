from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE
    )
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField()
    def __str__(self):
        return self.name
# https://medium.com/django-unleashed/implementing-multiple-file-uploads-in-django-e9b1833755ed
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
        related_name = 'images'
    )
    image_path = models.CharField(max_length = 255)
    image_file = models.FileField(upload_to='product_images/', default='product_images/productpic.jpg')
    def __str__(self):
        return self.image_path or str(self.image_file)