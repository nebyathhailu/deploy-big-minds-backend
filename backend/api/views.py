from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, ValidationError
from product.models import Product, VendorProduct
from payment.models import Payment
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from users.models import User
from .serializers import (
    ProductSerializer,
    VendorProductSerializer,
    PaymentSerializer,
    SubscriptionBoxSerializer,
    ScheduledItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    CartSerializer,
    CartItemSerializer,
)
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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'phone_number', 'location', 'shop_name']
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer_name = self.request.data.get('customer_name') or self.request.query_params.get('customer_name')
        cart = None
        if customer_name:
            try:
                user = User.objects.get(name=customer_name, type='customer')
                cart, _ = Cart.objects.get_or_create(customer=user)
            except User.DoesNotExist:
                raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        context['cart'] = cart
        return context
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny] 
    @action(detail=False, methods=['get'], url_path='by-customer')
    def get_cart_by_customer(self, request):
        customer_name = request.query_params.get('customer_name')
        if not customer_name:
            return Response(
                {"error": "customer_name query parameter is required"},
                status=400
            )
        try:
            user = User.objects.get(name=customer_name, type='customer')
        except User.DoesNotExist:
            raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        except User.MultipleObjectsReturned:
            raise ValidationError(
                f"Multiple customers found with name '{customer_name}'. Please use a unique identifier."
            )
        cart, created = Cart.objects.get_or_create(customer=user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=200)










