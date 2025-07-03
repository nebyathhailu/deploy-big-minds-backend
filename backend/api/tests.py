
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from products.models import Product
from subscription.models import SubscriptionBox, ScheduledItem


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = User.objects.create(
            name="Test Vendor",
            phone_number="123456789",
            password_hash="somerandomhash",
            location="Test Location",
            shop_name="Test Shop",
            till_number=1001,
            type="vendor",
        )
        self.product = Product.objects.create(
            name="Test Product",
            category="Test Category",
            product_image="https://example.com/test.jpg", 
            unit="kg"
        )
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=10.0,
            quantity=5,
            description="Test vendor product"
        )

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('vendor-products', response.data)

    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_create(self):
        data = {
            "name": "Another Product",
            "category": "Another Category",
            "product_image": "https://example.com/test2.jpg", 
            "unit": "pcs"
        }
        response = self.client.post(reverse('product-list'), data, format='json')
        print("Product create response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_detail(self):
        response = self.client.get(reverse('product-detail', args=[self.product.product_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_vendor_product_list(self):
        response = self.client.get(reverse('vendorproduct-list'))
        print("VendorProduct list response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_vendor_product_create(self):
        product = Product.objects.create(
            name="New Product",
            category="Category",
            product_image="https://example.com/test3.jpg", 
            unit="pcs"
        )
        data = {
            "vendor_id": self.vendor.user_id,
            "product_id": product.product_id,
            "price": 20.0,
            "quantity": 10,
            "description": "Another vendor product"
        }
        response = self.client.post(reverse('vendorproduct-list'), data, format="json")
        print("VendorProduct create response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorProduct.objects.count(), 2)

    def test_vendor_product_detail(self):
        response = self.client.get(reverse('vendorproduct-detail', args=[self.vendor_product.product_details_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.vendor_product.description)

class OrderPaymentAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", till_number= "34567899")
        self.buyer = Buyer.objects.create(name="Test Buyer")
    def test_create_order(self):
        url = reverse('order-list')
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": "500.00",
            "status": "approved"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['total_price'], "500.00")
    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data or isinstance(response.data, list))
    def test_create_payment(self):
        url = reverse('payment-list')
        data = {
            "order_id": self.order.pk,
            "method": "credit_card",
            "status": "pending",
            "amount": "1000.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(response.data['amount'], "1000.00")
    def test_list_payments(self):
        Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data or isinstance(response.data, list))
    def test_retrieve_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "500.00")
    def test_update_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        data = {
            "order_id": self.order.pk,
            "method": "credit_card",
            "status": "pending",
            "amount": "750.00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(payment.amount, 750.00)
    def test_delete_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=payment.pk).exists())



