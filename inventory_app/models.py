from django.db import models
from django.contrib.auth.models import User  # Import User model


class Category(models.Model):
    name = models.CharField(max_length=100, default='Uncategorized')  # Default value added

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, default='Unknown Supplier')  # Default value added
    contact_info = models.TextField(default='N/A')  # Default value added

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Image field added

    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.CharField(max_length=255, blank=True, null=True)  # Add this line
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    last_status_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.status}"
