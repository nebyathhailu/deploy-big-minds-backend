from django.test import TestCase
from users.models import Vendor, Buyer
from payments.models import Payment

class PaymentModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Test City",
            shop_name="Test Shop",
            till_number=123456,  
        )
        self.buyer = Buyer.objects.create(
            name="Test Buyer",
            password_hash="buyerhashedpassword",
            location="Buyer City",
            phone_number="0987654321",
        )
      
    def test_create_payment(self):
        self.assertEqual(payment.method, "Credit Card")
        self.assertEqual(payment.status, "Completed")
        self.assertEqual(float(payment.amount), 99.99)
        self.assertIsNotNone(payment.created_at)
    def test_payment_str(self):
        expected_str = f"Payment {payment.payment_id}  ({payment.status})"
        self.assertEqual(str(payment), expected_str)

  
     