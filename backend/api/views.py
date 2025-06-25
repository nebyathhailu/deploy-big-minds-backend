<<<<<<< HEAD
from django.shortcuts import render
from rest_framework import viewsets
from orders.models import Order, OrderItem
from .serializers import OrderSerializers, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
=======
from rest_framework import viewsets
from users.models import User
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']  
    search_fields = ['name', 'phone_number', 'location', 'shop_name']
>>>>>>> c5049ea63d7bfe85ce3066523e06663a6f3bd4e8
