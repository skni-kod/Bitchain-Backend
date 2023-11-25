"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user APi"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'full_name': 'Test User',
            'nick_name': 'Test',
            'date_of_birth': '1990-01-01',
            'pesel': '90010100000',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_existing_pesel(self):
        """Test creating a user with an existing PESEL fails"""
        create_user(
            email='existing@example.com',
            password='existing123',
            full_name='Existing User',
            nick_name='Existing',
            date_of_birth='1990-01-01',
            pesel='90010100000',  # PESEL that already exists in the database
        )
        payload = {
            'email': 'new@example.com',
            'password': 'new123',
            'full_name': 'New User',
            'nick_name': 'New',
            'date_of_birth': '1991-01-01',
            'pesel': '90010100000',  # Same PESEL as the existing user
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_existing_nick_name(self):
        """Test creating a user with an existing nick_name fails"""
        create_user(
            email='existing@example.com',
            password='existing123',
            full_name='Existing User',
            nick_name='existing_nick',
            date_of_birth='1990-01-01',
            pesel='90010111111',
        )
        payload = {
            'email': 'new@example.com',
            'password': 'new123',
            'full_name': 'New User',
            'nick_name': 'existing_nick',  # Same nick_name as the existing user
            'date_of_birth': '1991-01-01',
            'pesel': '90010222222',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_existing_email(self):
        """Test creating a user with an existing email fails"""
        create_user(
            email='existing@example.com',  # Existing email address
            password='existing123',
            full_name='Existing User',
            nick_name='existing',
            date_of_birth='1990-01-01',
            pesel='90010333333',
        )
        payload = {
            'email': 'existing@example.com',  # Same email as the existing user
            'password': 'new123',
            'full_name': 'New User',
            'nick_name': 'new_nick',
            'date_of_birth': '1991-01-01',
            'pesel': '90010444444',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_invalid_pesel(self):
        """Test creating a user with an invalid PESEL fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'full_name': 'Test User',
            'nick_name': 'Test',
            'date_of_birth': '1990-01-01',
            'pesel': '12345',  # PESEL with less than 11 digits
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload['pesel'] = 'asdl12asdl12'  # PESEL with non-numeric characters
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_invalid_date_of_birth_format(self):
        """Test creating a user with an invalid date of birth format fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'full_name': 'Test User',
            'nick_name': 'Test',
            'date_of_birth': '1990/01/01',  # Incorrect date format
            'pesel': '12345678901',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload['date_of_birth'] = '01-01-1990'  # Incorrect date format
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload['date_of_birth'] = '1990-13-01'  # Incorrect month format
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload['date_of_birth'] = '1990-01-32'  # Incorrect day format
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {
            'email': 'test@example.com',
            'password': '123a5d',  # Password with less than 8 characters
            'full_name': 'Test User',
            'nick_name': 'Test',
            'date_of_birth': '1990-01-01',
            'pesel': '90010100000',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        user_details = {
            'email': 'test@example.com',
            'password': 'testing123',
            'full_name': 'Test User',
            'nick_name': 'Test',
            'date_of_birth': '1990-01-01',
            'pesel': '90010100000',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_bad_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@example.com', password='testing123', full_name='Test User', nick_name='Test',
                    date_of_birth='1990-01-01', pesel='90010100000')

        payload = {
            'email': 'test@example.com',
            'password': 'wrong_password',  # Incorrect password
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_blank_password(self):
        """Test that token is not created if password is blank"""
        res = self.client.post(TOKEN_URL, {'email': 'test@example.com', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testing123',
            full_name='Test User',
            nick_name='Test',
            date_of_birth='1990-01-01',
            pesel='90010100000',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'full_name': self.user.full_name,
            'nick_name': self.user.nick_name,
            'date_of_birth': self.user.date_of_birth,
            'pesel': self.user.pesel,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'full_name': 'New Name',
            'nick_name': 'New Nick',
            'date_of_birth': '1991-01-01',
            'password': 'newpassword123',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, payload['full_name'])
        self.assertEqual(self.user.nick_name, payload['nick_name'])
        self.assertEqual(self.user.date_of_birth.strftime('%Y-%m-%d'), payload['date_of_birth'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)