<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items',OrderItemViewSet, basename='order-items')

urlpatterns = [
    path("", include(router.urls))
]
=======
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = router.urls
>>>>>>> c5049ea63d7bfe85ce3066523e06663a6f3bd4e8
