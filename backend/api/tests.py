from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from products.models import Product
from subscription.models import SubscriptionBox, ScheduledItem

class SubscriptionBoxAPITest(APITestCase):
    def setUp(self):
        self.buyer = User.objects.create(name='Buyer', type='customer')
        self.vendor = User.objects.create(name='Vendor', type='vendor')
        self.product = Product.objects.create(name='Carrot')
        self.box = SubscriptionBox.objects.create(
            buyer=self.buyer,
            vendor=self.vendor,
            name="Test Box",
            frequency="weekly",
            price=100,
            status="active"
        )
        self.scheduled_item = ScheduledItem.objects.create(
            product=self.product,
            schedule=self.box,
            price_per_unit=5.00,
            quantity=3,
            unit='kg'
        )

    def test_list_subscription_boxes(self):
        url = reverse('subscriptionbox-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.box.name)

    def test_create_subscription_box(self):
        url = reverse('subscriptionbox-list')
        data = {
            "buyer": self.buyer.pk,
            "vendor": self.vendor.pk,
            "name": "Weekly Fruits",
            "frequency": "weekly",
            "price": 200,
            "status": "active"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Weekly Fruits")

    def test_retrieve_subscription_box(self):
        url = reverse('subscriptionbox-detail', args=[self.box.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.box.name)

    def test_update_subscription_box(self):
        url = reverse('subscriptionbox-detail', args=[self.box.pk])
        data = {
            "buyer": self.buyer.pk,
            "vendor": self.vendor.pk,
            "name": "Updated Box",
            "frequency": "monthly",
            "price": 150,
            "status": "inactive"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Box")
        self.assertEqual(response.data['frequency'], "monthly")

    def test_delete_subscription_box(self):
        url = reverse('subscriptionbox-detail', args=[self.box.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubscriptionBox.objects.filter(pk=self.box.pk).exists())

    def test_list_scheduled_items(self):
        url = reverse('scheduleditem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quantity'], self.scheduled_item.quantity)

    def test_create_scheduled_item(self):
        url = reverse('scheduleditem-list')
        data = {
            "product": self.product.pk,
            "schedule": self.box.pk,
            "price_per_unit": 7.50,
            "quantity": 5,
            "unit": "kg"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 5)

    def test_retrieve_scheduled_item(self):
        url = reverse('scheduleditem-detail', args=[self.scheduled_item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], self.scheduled_item.quantity)

    def test_update_scheduled_item(self):
        url = reverse('scheduleditem-detail', args=[self.scheduled_item.pk])
        data = {
            "product": self.product.pk,
            "schedule": self.box.pk,
            "price_per_unit": 12.00,
            "quantity": 9,
            "unit": "kg"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 9)
        self.assertEqual(float(response.data['price_per_unit']), 12.00)

    def test_delete_scheduled_item(self):
        url = reverse('scheduleditem-detail', args=[self.scheduled_item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ScheduledItem.objects.filter(pk=self.scheduled_item.pk).exists())