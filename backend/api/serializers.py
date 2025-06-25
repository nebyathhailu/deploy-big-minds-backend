from rest_framework import serializers
from payment.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Payment
        fields = ['payment_id', 'method', 'status', 'amount']
