from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, BuyerViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'buyers', BuyerViewSet)

urlpatterns = router.urls