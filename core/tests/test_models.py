from django.test import TestCase
from django.contrib.auth import get_user_model
from authcore.models import UserClient
import core.models as models
from unittest.mock import patch


def sample_user(email='test@test.com', username='test', password='test'):
    return UserClient.objects.create_client(email=email, username=username, password=password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with a successful email"""
        username = 'test'
        email = 'test@test.com'
        password = 'test'
        user_client = UserClient.objects.create_client(email=email, password=password, username=username)
        self.assertEqual(user_client.email, email)
        self.assertTrue(user_client.check_password(password))
        user_client.delete()

    def test_create_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@test.com'
        user_client = UserClient.objects.create_client(email=email, username='test', password='test')
        self.assertEqual(user_client.email, email.lower())
        user_client.delete()

    def test_create_user_invalid_email(self):
        """Test creating a user with an invalid email"""
        with self.assertRaises(ValueError):
            UserClient.objects.create_user(None, 'test', 'test')

    def test_create_superuser_successful(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        user.delete()

    def test_create_customer(self):
        """Test creating a new customer"""
        user_client = sample_user()
        customer = models.Customer.objects.create(id=user_client.id, user=user_client)
        self.assertEqual(user_client.id, customer.id)
        user_client.delete()
        customer.delete()

    def test_create_address_for_customer(self):
        """Test creating an address for customer"""
        user_client = sample_user()
        customer = models.Customer.objects.create(id=user_client.id, user=user_client)
        address = models.Address.objects.create(
            customer=customer,
            street='test street',
            street_number='test street number',
            city='test',
            zipcode='test'
        )
        self.assertEqual(customer.id, address.customer.id)
        self.assertEqual('test street', address.street)

    def test_create_category_product(self):
        """Test creating a product"""
        category = models.Category.objects.create(
            name='test',
            slug='test-slug'
        )
        product = models.Product.objects.create(
            title='title',
            description='description',
            price=1.0,
            stock=20,
            category=category,
            image=None
        )
        self.assertEqual(category.name, 'test')
        self.assertEqual(product.title, 'title')

    @patch('uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test that product image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, 'test-product.jpg')
        exp_path = f'uploads/product/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
