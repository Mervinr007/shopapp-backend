from django.contrib import admin
from .models import Inventory, Shop, Product,UserPreference
admin.site.register(Shop)
admin.site.register(Product)    
admin.site.register(Inventory)
admin.site.register(UserPreference)