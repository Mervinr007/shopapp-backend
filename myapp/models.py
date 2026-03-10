from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
class Shop(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=255)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    image=models.ImageField(upload_to='shop_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    weight = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                Lower('weight'),
                name='unique_product_variant_case_insensitive'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.weight})"
    
class Inventory(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='inventory')
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)
    stock_count=models.PositiveBigIntegerField()
    
    def clean(self):
        if self.selling_price > self.product.mrp:
            raise ValidationError("Selling price cannot be greater than MRP.")
    
    class Meta:
        unique_together = ('product', 'shop')
    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"
    
class UserPreference(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    def __str__(self):
        return f"{self.user.username} - {self.theme}"