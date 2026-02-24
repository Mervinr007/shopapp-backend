from django.urls import path,include
from . import views     
  
urlpatterns = [
  path('shops/',views.shop_list, name='shop-list'),
  path('shops/<int:pk>/',views.shop_detail, name='shop-detail'),
  path('products/',views.product_list, name='product-list'),
  path('products/<int:pk>/',views.product_detail, name='product-detail'),
  path('change-password/', views.change_password, name='change-password'),
  path('register/', views.register, name='register'),
  path('check-auth/', views.check_auth, name='check-auth'),
  ]