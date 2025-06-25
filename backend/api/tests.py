from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from products.models import Product
from orders.models import Order, OrderItem
from subscription.models import SubscriptionBox, ScheduledItem
from django.test import TestCase

class OrderAPITests(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Nairobi",
            shop_name="Vendor Shop",
            till_number=1001,
            type="vendor"
        )
        self.buyer = User.objects.create(
            name="Test Buyer",
            password_hash="hashedpassword",
            location="Nairobi",
            phone_number="0987654321",
            type="customer"
        )
        self.product = Product.objects.create(
            name="Test Product",
            category="Groceries",
            unit="kg",
        )
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=200.00,
            status="Pending"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_order=100.00
        )

    def test_list_orders(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_order(self):
        url = reverse('orders-list')
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": 300.00,
            "status": "Confirmed"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_price"], "300.00")

    def test_retrieve_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_id"], self.order.pk)

    def test_update_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": 250.00,
            "status": "Shipped"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Shipped")

    def test_delete_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())


class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Nairobi",
            shop_name="Vendor Shop",
            till_number=1002,
            type="vendor"
        )
        self.buyer = User.objects.create(
            name="Test Buyer",
            password_hash="hashedpassword",
            location="Nairobi",
            phone_number="0987654322",
            type="customer"
        )
        self.product = Product.objects.create(
            name="Mango",
            category="Fruit",
            unit="Bunch",
        )
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=150.00,
            status="Pending"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price_at_order=150.00
        )

    def test_list_order_items(self):
        url = reverse('order-items-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_order_item(self):
        url = reverse('order-items-list')
        data = {
            "order": self.order.pk,
            "product": self.product.pk,
            "quantity": 3,
            "price_at_order": 300.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"], 3)

    def test_retrieve_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["item_id"], self.order_item.pk)

    def test_update_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        data = {
            "order": self.order.pk,
            "product": self.product.pk,
            "quantity": 5,
            "price_at_order": 750.00
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 5)

    def test_delete_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())


class SubscriptionBoxAPITest(TestCase):
   def setUp(self):
       self.client = APIClient()
       self.buyer = User.objects.create(
           name="Test Buyer",
           password_hash="password",
           location="Test Location",
           phone_number="123456789",
           type="customer"
       )
       self.vendor = User.objects.create(
           name="Test Vendor",
           phone_number="987654321",
           password_hash="password",
           profile_picture=None,
           location="Vendor Location",
           shop_name="Vendor Shop",
           till_number=111222,
           type="vendor"
       )
       self.product = Product.objects.create(
           name="Test Product",
           category="Fruits",
           product_image=None,
           unit="kg"
       )
       self.box = SubscriptionBox.objects.create(
           buyer=self.buyer,
           vendor=self.vendor,
           name="Fruit Box",
           frequency="monthly",
           price=29.99,
           status="active"
       )
       self.box_data = {
           "buyer": self.buyer.pk,
           "vendor": self.vendor.pk,
           "name": "Veggie Box",
           "frequency": "monthly",
           "price": "39.99",
           "status": "active"
       }
       self.scheduleditem_data = {
           "product": self.product.pk,
           "schedule": self.box.schedule_id,
           "price_per_unit": "2.50",
           "quantity": 5,
           "unit": "kg"
       }

   def test_list_subscription_boxes(self):
       response = self.client.get("/api/subscriptions/")
       self.assertEqual(response.status_code, 200)
       self.assertTrue(len(response.data) >= 1)

   def test_create_subscription_box(self):
       response = self.client.post("/api/subscriptions/", self.box_data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data["name"], "Veggie Box")

   def test_retrieve_subscription_box(self):
       response = self.client.get(f"/api/subscriptions/{self.box.schedule_id}/")
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.data["name"], self.box.name)

   def test_delete_subscription_box(self):
       response = self.client.delete(f"/api/subscriptions/{self.box.schedule_id}/")
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       self.assertFalse(SubscriptionBox.objects.filter(schedule_id=self.box.schedule_id).exists())

   def test_create_scheduled_item(self):
       response = self.client.post("/api/scheduled-items/", self.scheduleditem_data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data["quantity"], 5)
       self.assertEqual(response.data["unit"], "kg")

   def test_list_scheduled_items(self):
       item = ScheduledItem.objects.create(
           product=self.product,
           schedule=self.box,
           price_per_unit=2.5,
           quantity=2,
           unit='kg'
       )
       response = self.client.get("/api/scheduled-items/")
       self.assertEqual(response.status_code, 200)
       self.assertTrue(len(response.data) >= 1)

   def test_retrieve_scheduled_item(self):
       item = ScheduledItem.objects.create(
           product=self.product,
           schedule=self.box,
           price_per_unit=2.5,
           quantity=2,
           unit='kg'
       )
       response = self.client.get(f"/api/scheduled-items/{item.scheduled_item_id}/")
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.data["quantity"], 2)

   def test_delete_scheduled_item(self):
       item = ScheduledItem.objects.create(
           product=self.product,
           schedule=self.box,
           price_per_unit=2.5,
           quantity=2,
           unit='kg'
       )
       response = self.client.delete(f"/api/scheduled-items/{item.scheduled_item_id}/")
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       self.assertFalse(ScheduledItem.objects.filter(scheduled_item_id=item.scheduled_item_id).exists())

class VendorAPITest(APITestCase):
    def test_create_vendor(self):
        # Make sure your URLs and views support this, or update to the current users endpoint
        url = reverse('user-list')  # update to your current user endpoint
        data = {
            "name": "Test Vendor",
            "phone_number": "123456789",
            "password_hash": "hash",
            "location": "Test Location",
            "shop_name": "Shop",
            "till_number": 123,
            "type": "vendor"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)