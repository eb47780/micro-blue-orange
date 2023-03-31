from django.test import TestCase
from django.urls import reverse
from authcore.models import UserClient
from core.models import Customer
from rest_framework.test import APIClient
from rest_framework import status

CLIENT_URL = reverse("core:client-list-create-view")
TOKEN_URL = reverse("core:token_obtain_pair")


def create_user(**params):
    user_client = UserClient.objects.create_client(**params)
    params['phone'] = 'test'
    params.pop('username')
    params.pop('password')
    customer = Customer.objects.create(id=user_client.id, user=user_client, **params)
    return customer


class UsersApiTests(TestCase):
    def setUp(self) -> None:
        self.payload = {"username": "test", "email": "test@test.com", "password": "test"}
        self.client = APIClient()

    def test_user_signup(self):
        """Test that a user is created and returns user content, else just check if user already exists"""
        body = {
            "name": "test",
            "email": "test@test.com",
            "password": "test",
            "phone": "+38349433122"
        }
        res = self.client.post(CLIENT_URL, body)
        self.assertIn('id', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = Customer.objects.filter(id=res.data['id'])
        user.delete()

    def test_create_jwt_token_for_user(self):
        """Test that token is created for user"""
        user = create_user(**self.payload)
        res = self.client.post(TOKEN_URL, {"email": "test@test.com", "password": "test"})
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user.delete()

    def test_create_jwt_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        user = create_user(**self.payload)
        payload = {'email': 'test@test.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        user.delete()

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': 'test'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users to check profile"""
        user = create_user(**self.payload)
        CLIENT_DETAIL = reverse("core:client-detail-update", args=[user.id])
        res = self.client.get(CLIENT_DETAIL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        user.delete()