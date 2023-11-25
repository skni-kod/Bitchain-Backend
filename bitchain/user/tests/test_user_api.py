"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

import datetime

CREATE_USER_URL = reverse('user:create')


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
        existing_user = create_user(
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
        existing_user = create_user(
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
        existing_user = create_user(
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