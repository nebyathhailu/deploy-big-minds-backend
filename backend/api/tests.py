from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User  
from product.models import Product, VendorProduct  

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