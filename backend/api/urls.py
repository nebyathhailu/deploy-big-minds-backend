from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VendorProductViewSet,SubscriptionBoxViewSet, ScheduledItemViewSet, PaymentViewSet, OrderViewSet, OrderItemViewSet,  UserViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'vendor-products', VendorProductViewSet, basename='vendorproduct')
urlpatterns = [
    path('', include(router.urls)),
]

router.register(r'subscriptions', SubscriptionBoxViewSet, basename='subscriptionbox')
router.register(r'scheduled-items', ScheduledItemViewSet, basename='scheduleditem')

router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items',OrderItemViewSet, basename='order-items')

router.register(r'users', UserViewSet)
router.register(r'payments', PaymentViewSet,basename='payments')  

