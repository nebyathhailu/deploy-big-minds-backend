from django.test import TestCase
from .models import Payment
from decimal import Decimal

class PaymentModelTest(TestCase):
    def test_create_payment(self):
        payment = Payment.objects.create(
            method="Mpesa",
            status="Completed",
            amount=Decimal("1500.00")
        )
        self.assertIsNotNone(payment.payment_id)
        self.assertEqual(payment.method, "Mpesa")
        self.assertEqual(payment.status, "Completed")
        self.assertEqual(payment.amount, Decimal("1500.00"))

    def test_str_representation(self):
        payment = Payment.objects.create(
            method="Card",
            status="Pending",
            amount=Decimal("500.00")
        )
        self.assertEqual(str(payment), f"Payment {payment.payment_id} (Pending)")

    def test_created_at_auto_now(self):
        payment = Payment.objects.create(
            method="Cash",
            status="Failed",
            amount=Decimal("0.00")
        )
     
        from django.utils import timezone
        now = timezone.now()
        self.assertTrue(abs((now - payment.created_at).total_seconds()) < 10)