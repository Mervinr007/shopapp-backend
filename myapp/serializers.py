from psycopg2 import IntegrityError
from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_mrp(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "MRP must be a positive number."
            )
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "This product variant already exists in catalogue."
            )
class ShopSerializer(serializers.ModelSerializer):
    total_products=serializers.IntegerField(read_only=True)
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Shop
        fields = '__all__'
class InventorySerializer(serializers.ModelSerializer):
   
    product = ProductSerializer(read_only=True)

    
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    shop_name = serializers.ReadOnlyField(source='shop.name')
    shop_owner = serializers.ReadOnlyField(source='shop.owner.username')

    class Meta:
        model = Inventory
        fields = [
            'id',
            'product',
            'product_id',   
            'shop',
            'shop_name',
            'shop_owner',
            'selling_price',
            'stock_count'
        ]

    def validate_stock_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock count cannot be negative.")
        return value

    def validate_selling_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Selling price must be positive.")
        return value
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
class OwnerShopSerializer(serializers.ModelSerializer):
    total_products=serializers.IntegerField()
    class Meta:
        model = Shop
        fields = '__all__'
        