from django.contrib import admin
from .models import Inventory, Shop, Product
admin.site.register(Shop)
admin.site.register(Product)    
admin.site.register(Inventory)
