from rest_framework import serializers
from product.models import Product, VendorProduct
from users.models import User 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'product_image', 'unit']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['user_id', 'name']

class VendorProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type='vendor'), source='vendor', write_only=True
    )
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    class Meta:
        model = VendorProduct
        fields = [
            'product_details_id', 'vendor', 'vendor_id', 'product', 'product_id',
            'price', 'quantity', 'description', 'added_on', 'updated_at'
        ]