from rest_framework import viewsets
from product.models import Product, VendorProduct
from .serializers import ProductSerializer, VendorProductSerializer
from payment.models import Payment
from .serializers import PaymentSerializer
from subscription.models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer
from django.shortcuts import render
from orders.models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from users.models import User
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        qs = self.queryset
        if user_id:
            qs = qs.filter(buyer__user_id=user_id)
        return qs
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class=OrderItemSerializer

    def get_queryset(self):
        order_id = self.request.query_params.get('order')
        qs = self.queryset
        if order_id:
            qs = qs.filter(order_id=order_id)
        return qs

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']  
    search_fields = ['name', 'phone_number', 'location', 'shop_name']
