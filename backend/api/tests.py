from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import Vendor
from .models import Product, VendorProduct
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import tempfile

def get_temporary_image():
    image = Image.new('RGB', (100, 100), color = 'red')
    tmp_file = BytesIO()
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return SimpleUploadedFile('test.jpg', tmp_file.read(), content_type='image/jpeg')

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image = get_temporary_image()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="123456789",
            password_hash="somerandomhash",
            location="Test Location",
            shop_name="Test Shop",
            till_number=1001,
        )
        self.product = Product.objects.create(
            name="Test Product",
            category="Test Category",
            product_image=self.image,
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
        image = get_temporary_image()
        data = {
            "name": "Another Product",
            "category": "Another Category",
            "product_image": image,
            "unit": "pcs"
        }
        response = self.client.post(reverse('product-list'), data, format='multipart')
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
            product_image=self.image,
            unit="pcs"
        )
        data = {
            "vendor_id": self.vendor.vendor_id,
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
        response = self.client.get(reverse('vendorproduct-detail', args=[self.vendor_product.product_ddetails_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.vendor_product.description)