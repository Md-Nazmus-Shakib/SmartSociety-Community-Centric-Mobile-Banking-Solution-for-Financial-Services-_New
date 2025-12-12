from django.db import models
from users.models import User

class Product(models.Model):
    merchant = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # ensure quantity always has a value to avoid NOT NULL errors
    product_quntity = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    def __str__(self):
        return f"{self.product_name} - {self.merchant.user.username}"
# Create your models here.
