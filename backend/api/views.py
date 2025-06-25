from rest_framework import viewsets
from subscription.models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer