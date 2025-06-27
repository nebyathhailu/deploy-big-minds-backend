from django.db import models
from users.models import User

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class VendorProduct(models.Model):
    product_ddetails_id = models.AutoField(primary_key=True)
    
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.product.name}"