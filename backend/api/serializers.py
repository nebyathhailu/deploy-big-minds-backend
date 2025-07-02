from rest_framework import serializers
from product.models import Product, VendorProduct
from users.models import User 
from payment.models import Payment
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem


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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'method', 'status', 'amount', 'created_at']

class SubscriptionBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBox
        fields = "__all__"

class ScheduledItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledItem
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',
        write_only=True
    )
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

